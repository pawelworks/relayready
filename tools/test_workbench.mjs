// Pure-engine checks plus reproducible vectors for independent Python parity.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { webcrypto } from "node:crypto";
import { fileURLToPath } from "node:url";
import { resolve, dirname } from "node:path";
import { clone, serialize, parseJSON, timestamp, prepareTemplate, evaluate,
  makeBundle, importBundle, compareBundles, suiteCases, validateObservation } from "../out/workbench-engine.mjs";
if (!globalThis.crypto) globalThis.crypto = webcrypto;
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const fixtures = JSON.parse(readFileSync(resolve(root, "out/demo-fixtures.json"), "utf8"));
const templates = await Promise.all(fixtures.scenarios.map(prepareTemplate));
const clean = templates.find(t => t.id === "clean");
const cases = suiteCases(templates);
for (const [name, mutate, expected, now] of [
  ["Unknown revision", o => { o.resources[0].revision = null; }, "recheck"],
  ["Unknown bytes", o => { o.run_inputs[0].digest = null; }, "recheck"],
  ["Missing bytes", o => { o.run_inputs = []; }, "recheck"],
  ["Missing operation", o => { o.effects = []; }, "recheck"],
  ["Already applied", o => { o.effects[0].status = "applied"; }, "escalate"],
  ["Unexpected resource", o => { o.resources.push({id:"extra",revision:"1"}); }, "escalate"],
  ["Unexpected input", o => { o.run_inputs.push({name:"extra",digest:null}); }, "escalate"],
  ["Unexpected operation", o => { o.effects.push({id:"extra",status:"unknown",evidence:null}); }, "escalate"],
  ["Old observation", o => { o.observed_at = "2026-09-20T11:59:00Z"; }, "recheck"],
  ["Future observation", o => { o.observed_at = "2026-09-20T12:06:00Z"; }, "recheck"],
  ["Before handoff", () => {}, "recheck", "2026-09-20T11:59:00Z"],
  ["Millisecond clock", () => {}, "resume", "2026-09-20T12:05:00.123Z"],
  ["Equivalent offset", () => {}, "resume", "2026-09-20T15:05:00+03:00"],
]) {
  const observation = clone(clean.observation); mutate(observation);
  cases.push({name,template:clean,observation,expected,now:now || clean.receipt.evaluated_at});
}
const vectors = [];
for (const c of cases) {
  const raw = serialize(c.observation);
  const {assessment} = await evaluate(c.template, raw, c.now);
  assert.equal(assessment.decision, c.expected, c.name);
  const bundle = makeBundle(c.template, raw, assessment);
  vectors.push({name:c.name,bundle});
  if (!c.name.startsWith("Unexpected") && c.name !== "Wrong checkpoint binding") {
    assert.deepEqual((await importBundle(serialize(bundle),templates)).assessment, assessment);
  } else await assert.rejects(importBundle(serialize(bundle),templates));
}
for (const source of ['{"x":1,"x":2}', '{"x":1,"\\u0078":2}', '{"x":{"a":0,"a":1}}', '{"x":NaN}']) assert.throws(() => parseJSON(source));
assert.deepEqual(parseJSON('{"a":{"x":1},"b":{"x":2},"quoted":"{\\\"x\\\":2}"}').a,{x:1});
for (const clock of ["2026-02-30T12:00:00Z","0000-01-01T00:00:00Z","0001-01-01T00:00:00+01:00","9999-12-31T23:59:59-01:00","2026-09-20T12:00:00.1234Z"]) assert.throws(() => timestamp(clock));
for (const mutate of [
  o => { o.checkpoint_sha256 = [o.checkpoint_sha256]; },
  o => { o.run_inputs[0].digest = [o.run_inputs[0].digest]; },
  o => { o.resources[0].revision = String.fromCharCode(28,133); },
  o => { o.resources.push(clone(o.resources[0])); },
  o => { o.effects[0].status = "approved"; },
  o => { o.extra = true; },
]) { const o = clone(clean.observation); mutate(o); assert.throws(() => validateObservation(o)); }
const original = vectors[0].bundle;
const tampered = clone(original); tampered.assessment.decision = "escalate";
await assert.rejects(importBundle(serialize(tampered),templates), /recomputation/);
const changed = clone(original); changed.artifacts.handoff += "\n";
await assert.rejects(importBundle(serialize(changed),templates), /exact/);
const unknown = vectors.find(v => v.name === "Unknown revision").bundle;
const missing = vectors.find(v => v.name === "Missing resource").bundle;
assert.ok(compareBundles(original,unknown).rows.some(r => r.after === null));
assert.ok(compareBundles(unknown,missing).rows.some(r => r.after === "(absent)"));
assert.equal(original.assessment.decision,"resume");
if (process.argv.includes("--vectors")) console.log(serialize(vectors));
else console.log("Workbench checks passed: " + vectors.length + " decision vectors, imports, tamper detection, strict JSON, clock bounds and comparison semantics.");
