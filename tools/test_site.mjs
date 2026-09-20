// Dependency-free behavioral smoke checks for the static recorded-fixture UI.
// This is not a layout engine; responsive visual QA is a separate browser check.
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import vm from "node:vm";
import { createHash } from "node:crypto";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(resolve(root, "out/index.html"), "utf8");
const source = readFileSync(resolve(root, "out/app.js"), "utf8");
const fixtures = JSON.parse(readFileSync(resolve(root, "out/demo-fixtures.json"), "utf8"));
const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
for (const page of ["index.html", "workbench.html"]) {
  const text = readFileSync(resolve(root, "out", page), "utf8");
  for (const [, link] of text.matchAll(/(?:href|src)="([^"]+)"/g)) {
    if (/^(?:data:|https?:)/.test(link)) continue;
    const [file, anchor] = link.split("#");
    const path = resolve(root, "out", file || page);
    assert.ok(existsSync(path), page + ": missing " + link);
    if (anchor) assert.ok(readFileSync(path,"utf8").includes('id="' + anchor + '"'), page + ": missing anchor " + link);
  }
}
for (const [, link] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
  if (link.startsWith("#")) assert.ok(ids.has(link.slice(1)), `Missing anchor: ${link}`);
  else if (!/^(?:data:|https?:)/.test(link)) assert.ok(existsSync(resolve(root, "out", link)), `Missing local file: ${link}`);
}

class Element {
  constructor() {
    this.textContent = "";
    this.disabled = true;
    this.value = "";
    this.attributes = new Map();
    this.handlers = new Map();
    this.children = [];
    this.dataset = {};
    this.classes = new Set();
    this.classList = {
      add: (...names) => names.forEach((name) => this.classes.add(name)),
      remove: (...names) => names.forEach((name) => this.classes.delete(name)),
      contains: (name) => this.classes.has(name),
      toggle: (name, enabled) => enabled ? this.classes.add(name) : this.classes.delete(name)
    };
  }
  set className(value) { this.classes = new Set(value.split(" ").filter(Boolean)); }
  get className() { return [...this.classes].join(" "); }
  setAttribute(key, value) { this.attributes.set(key, value); }
  addEventListener(type, handler) { this.handlers.set(type, handler); }
  replaceChildren(...children) { this.children = children; }
  append(...children) { this.children.push(...children); }
  focus() { this.focused = true; }
  querySelector(selector) { return this.nested[selector]; }
  trigger(type, event = {}) { return this.handlers.get(type)?.(event); }
}

async function createApp({ fail = false, reducedMotion = true } = {}) {
  const elements = new Map([...ids].map((id) => [`#${id}`, new Element()]));
  const artifact = new Element();
  elements.set("#artifactCode code", artifact);
  const sender = new Element();
  const receiver = new Element();
  sender.nested = { ".agent-state": new Element() };
  receiver.nested = { ".agent-state": new Element() };
  elements.set('[data-agent="sender"]', sender);
  elements.set('[data-agent="receiver"]', receiver);
  const timeline = Array.from({ length: 4 }, () => new Element());
  const checks = Array.from({ length: 4 }, () => {
    const item = new Element();
    item.nested = { span: new Element() };
    return item;
  });
  const tabs = ["handoff", "readback", "checkpoint", "observation", "receipt"].map((name) => {
    const tab = elements.get(`#tab-${name}`);
    tab.dataset.tab = name;
    return tab;
  });
  const arrays = new Map([
    ["#timeline li", timeline], ["#checks li", checks], ['[role="tab"][data-tab]', tabs]
  ]);
  let tool;
  let clipboard;
  const context = {
    document: {
      querySelector: (selector) => {
        assert.ok(elements.has(selector), `Missing selector ${selector}`);
        return elements.get(selector);
      },
      querySelectorAll: (selector) => arrays.get(selector),
      createElement: () => new Element()
    },
    window: {
      matchMedia: () => ({ matches: reducedMotion }),
      setTimeout, clearTimeout
    },
    navigator: {
      modelContext: { registerTool: (value) => { tool = value; } },
      clipboard: { writeText: async (value) => { clipboard = value; } }
    },
    fetch: async () => ({ ok: !fail, json: async () => fixtures }),
    AbortController,
    console
  };
  vm.runInNewContext(source, context, { filename: "out/app.js" });
  await new Promise(setImmediate);
  return { elements, tabs, tool, checks, artifact, get clipboard() { return clipboard; } };
}

const app = await createApp();
assert.ok(app.tool, "The standard navigator.modelContext entry point registered the replay tool");
assert.equal(app.elements.get("#scenario").children.length, fixtures.scenarios.length);
for (const fixture of fixtures.scenarios) {
  const output = JSON.parse((await app.tool.execute({ scenario: fixture.id })).content[0].text);
  assert.equal(output.decision, fixture.receipt.decision, fixture.id);
  assert.equal(output.status, "recorded");
  assert.equal(output.simulated, true);
  assert.deepEqual(output.reasons, fixture.receipt.reasons);
  assert.equal(app.elements.get("#decisionTitle").textContent.toLowerCase(), fixture.receipt.decision);
  assert.equal(app.artifact.textContent, fixture.receipt_raw ?? JSON.stringify(fixture.receipt, null, 2));
  assert.equal(app.elements.get("#decisionReasons").children.length, fixture.receipt.reasons.length);
  for (const [index, name] of ["handoff", "readback", "checkpoint", "observation", "receipt"].entries()) {
    const text = fixture[`${name}_raw`] ?? fixture[name];
    assert.equal(typeof text, "string", `${fixture.id}/${name} provides exact text`);
    app.tabs[index].trigger("click");
    await app.elements.get("#copyArtifact").trigger("click");
    assert.equal(app.clipboard, text, `${fixture.id}/${name} copies exact recorded text`);
    if (name !== "receipt") {
      const digest = `sha256:${createHash("sha256").update(app.clipboard, "utf8").digest("hex")}`;
      assert.equal(digest, fixture.receipt.bindings[`${name}_sha256`], `${fixture.id}/${name} bytes match the recorded binding`);
    }
  }
}
await assert.rejects(app.tool.execute({ scenario: "not-a-scenario" }), /Unknown/);

// Keyboard navigation updates both the selected tab and accessible panel label.
app.tabs[4].trigger("keydown", { key: "Home", preventDefault() {} });
assert.equal(app.tabs[0].attributes.get("aria-selected"), "true");
assert.equal(app.elements.get("#artifactCode").attributes.get("aria-labelledby"), "tab-handoff");
const selected = fixtures.scenarios.at(-1);
assert.equal(app.artifact.textContent, selected.handoff);
await app.elements.get("#copyArtifact").trigger("click");
assert.equal(app.clipboard, selected.handoff, "Copy preserves exact handoff bytes as text");

// Reset and scenario change must settle old callers and prevent stale completions.
const slow = await createApp({ reducedMotion: false });
const first = slow.tool.execute({ scenario: "clean" });
slow.elements.get("#resetRelay").trigger("click");
assert.equal(JSON.parse((await first).content[0].text).status, "cancelled");
assert.equal(slow.elements.get("#validationState").textContent, "PENDING");
const second = slow.tool.execute({ scenario: "clean" });
slow.elements.get("#scenario").value = "uncertain-effect";
slow.elements.get("#scenario").trigger("change");
assert.equal(JSON.parse((await second).content[0].text).status, "cancelled");
assert.equal(slow.elements.get("#decisionTitle").textContent, "One handoff. Three possible decisions.");
assert.equal(slow.artifact.textContent, fixtures.scenarios.find((scenario) => scenario.id === "uncertain-effect").handoff);

const unavailable = await createApp({ fail: true });
assert.equal(unavailable.elements.get("#validationState").textContent, "UNAVAILABLE");
assert.equal(unavailable.elements.get("#runRelay").disabled, true);
assert.equal(unavailable.tool, undefined);
console.log(`Static site checks passed: local links, ${fixtures.scenarios.length} recorded decisions, reason codes, exact-text copy and SHA-256 bindings, keyboard tabs, cancellation and fixture-load failure.`);
