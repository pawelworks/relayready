(() => {
  "use strict";

  const els = {
    scenario: document.querySelector("#scenario"),
    summary: document.querySelector("#scenarioSummary"),
    run: document.querySelector("#runRelay"),
    reset: document.querySelector("#resetRelay"),
    timeline: [...document.querySelectorAll("#timeline li")],
    checks: [...document.querySelectorAll("#checks li")],
    sender: document.querySelector('[data-agent="sender"]'),
    receiver: document.querySelector('[data-agent="receiver"]'),
    score: document.querySelector("#scoreValue"),
    scoreLabel: document.querySelector("#scoreLabel"),
    status: document.querySelector("#validationState"),
    elapsed: document.querySelector("#elapsed"),
    panel: document.querySelector("#artifactCode"),
    artifactMeta: document.querySelector("#artifactMeta"),
    artifact: document.querySelector("#artifactCode code"),
    tabs: [...document.querySelectorAll('[role="tab"][data-tab]')],
    copy: document.querySelector("#copyArtifact"),
    decision: document.querySelector("#decisionPanel"),
    decisionTitle: document.querySelector("#decisionTitle"),
    decisionSummary: document.querySelector("#decisionSummary"),
    reasons: document.querySelector("#decisionReasons")
  };
  const decisions = {
    resume: { title: "Resume", message: "The recorded observations satisfy the declared checks. The executor still owns authorization and conditional execution." },
    recheck: { title: "Recheck", message: "The recorded observations require another check before relying on this checkpoint." },
    escalate: { title: "Escalate", message: "The recorded observations include uncertainty or a pending decision that must be resolved before continuation." }
  };
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const scenarios = new Map();
  let activeRun = null;
  let copyTimer = null;
  let currentTab = "handoff";

  const stateLabel = (card) => card.querySelector(".agent-state");
  const currentScenario = () => scenarios.get(els.scenario.value);

  // Cancelling settles the pending wait, so callers (including WebMCP) never hang.
  function wait(ms, signal) {
    return new Promise((resolve) => {
      if (signal.aborted) { resolve(false); return; }
      const onAbort = () => { window.clearTimeout(timer); resolve(false); };
      const timer = window.setTimeout(() => {
        signal.removeEventListener("abort", onAbort);
        resolve(true);
      }, reducedMotion.matches ? 0 : ms);
      signal.addEventListener("abort", onAbort, { once: true });
    });
  }

  function showArtifact(name) {
    const scenario = currentScenario();
    if (!scenario) return;
    currentTab = name;
    els.tabs.forEach((tab) => {
      const selected = tab.dataset.tab === name;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    els.panel.setAttribute("aria-labelledby", `tab-${name}`);
    const value = scenario[name];
    const raw = scenario[`${name}_raw`];
    els.artifact.textContent = typeof raw === "string" ? raw : typeof value === "string" ? value : JSON.stringify(value, null, 2);
    els.artifactMeta.textContent = typeof raw === "string" || typeof value === "string"
      ? "Exact recorded UTF-8 artifact text. Copy preserves its formatting."
      : "JSON displayed with formatting. Receipt digests refer to the original recorded artifact bytes.";
    els.panel.scrollTop = 0;
    window.clearTimeout(copyTimer);
    els.copy.textContent = "Copy artifact";
  }

  function setStep(step) {
    els.timeline.forEach((item, index) => {
      item.classList.toggle("complete", index < step);
      item.classList.toggle("current", index === step && step < 4);
    });
    els.elapsed.textContent = `STEP ${step} / 4`;
  }

  function resetRelay() {
    if (activeRun) activeRun.controller.abort();
    activeRun = null;
    const scenario = currentScenario();
    if (!scenario) return;
    els.run.disabled = false;
    els.run.textContent = "▶ Run relay";
    els.sender.classList.add("active");
    els.sender.classList.remove("complete");
    els.receiver.classList.remove("active", "complete");
    stateLabel(els.sender).textContent = "READY";
    stateLabel(els.receiver).textContent = "WAITING";
    els.summary.textContent = scenario.summary;
    els.status.textContent = "PENDING";
    els.status.className = "pending";
    els.score.textContent = "—";
    els.score.className = "";
    els.scoreLabel.textContent = "waiting for replay";
    els.checks.forEach((item) => {
      item.classList.remove("reviewed");
      item.querySelector("span").textContent = "○";
    });
    els.decision.className = "decision-panel";
    els.decisionTitle.textContent = "One handoff. Three possible decisions.";
    els.decisionSummary.textContent = "Resume when declared checks are consistent, recheck changed state, or escalate uncertainty that needs a decision.";
    els.reasons.replaceChildren();
    setStep(0);
    showArtifact("handoff");
  }

  function inspectCheck(index) {
    els.checks[index].classList.add("reviewed");
    els.checks[index].querySelector("span").textContent = "✓";
    els.score.textContent = `${index + 1}/4`;
    els.scoreLabel.textContent = "artifact groups inspected";
  }

  function showDecision(scenario) {
    const receipt = scenario.receipt;
    const decision = decisions[receipt.decision];
    els.decision.className = `decision-panel decision-${receipt.decision}`;
    els.decisionTitle.textContent = decision.title;
    els.decisionSummary.textContent = decision.message;
    els.reasons.replaceChildren(...receipt.reasons.map((reason) => {
      const item = document.createElement("li");
      const code = document.createElement("code");
      const message = document.createElement("span");
      code.textContent = reason.code;
      message.textContent = reason.message;
      item.append(code, message);
      return item;
    }));
    els.score.textContent = decision.title;
    els.score.className = `result-${receipt.decision}`;
    els.scoreLabel.textContent = "recorded decision";
    els.status.textContent = "RECORDED";
    els.status.className = `result-${receipt.decision}`;
  }

  async function animateRelay(run, scenario) {
    const signal = run.controller.signal;
    const cancelled = () => ({ scenario: scenario.id, status: "cancelled", simulated: true });
    stateLabel(els.sender).textContent = "PREPARING";
    if (!await wait(650, signal)) return cancelled();
    setStep(1);
    els.sender.classList.remove("active");
    els.sender.classList.add("complete");
    stateLabel(els.sender).textContent = "ISSUED";
    els.receiver.classList.add("active");
    stateLabel(els.receiver).textContent = "READBACK";
    showArtifact("readback");
    inspectCheck(0);

    if (!await wait(750, signal)) return cancelled();
    setStep(2);
    stateLabel(els.receiver).textContent = "OBSERVING";
    showArtifact("checkpoint");
    inspectCheck(1);
    if (!await wait(500, signal)) return cancelled();
    showArtifact("observation");
    inspectCheck(2);

    if (!await wait(650, signal)) return cancelled();
    setStep(3);
    showArtifact("receipt");
    inspectCheck(3);
    if (!await wait(300, signal)) return cancelled();
    setStep(4);
    showDecision(scenario);
    els.receiver.classList.remove("active");
    els.receiver.classList.add("complete");
    stateLabel(els.receiver).textContent = "RECORDED";
    els.run.disabled = false;
    els.run.textContent = "↻ Replay scenario";
    if (activeRun === run) activeRun = null;
    return {
      scenario: scenario.id,
      status: "recorded",
      decision: scenario.receipt.decision,
      reasons: scenario.receipt.reasons,
      simulated: true,
      execution: "Replayed saved local Python validator output. No live validator or agent execution."
    };
  }

  function runRelay() {
    if (activeRun) return activeRun.promise;
    const scenario = currentScenario();
    if (!scenario) return Promise.resolve({ status: "unavailable" });
    resetRelay();
    const run = { controller: new AbortController(), promise: null };
    activeRun = run;
    els.run.disabled = true;
    els.run.textContent = "Replaying…";
    els.status.textContent = "REPLAYING";
    run.promise = animateRelay(run, scenario);
    return run.promise;
  }

  els.run.addEventListener("click", runRelay);
  els.reset.addEventListener("click", resetRelay);
  els.scenario.addEventListener("change", resetRelay);
  els.tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => showArtifact(tab.dataset.tab));
    tab.addEventListener("keydown", (event) => {
      let next;
      if (event.key === "ArrowRight") next = (index + 1) % els.tabs.length;
      else if (event.key === "ArrowLeft") next = (index - 1 + els.tabs.length) % els.tabs.length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = els.tabs.length - 1;
      else return;
      event.preventDefault();
      els.tabs[next].focus();
      showArtifact(els.tabs[next].dataset.tab);
    });
  });
  els.copy.addEventListener("click", async () => {
    const copiedText = els.artifact.textContent;
    const copiedTab = currentTab;
    const copiedScenario = currentScenario();
    try {
      await navigator.clipboard.writeText(copiedText);
      if (copiedTab !== currentTab || copiedScenario !== currentScenario()) return;
      els.copy.textContent = "Copied";
    } catch {
      if (copiedTab !== currentTab || copiedScenario !== currentScenario()) return;
      els.copy.textContent = "Select text to copy";
      els.panel.focus();
      const selection = window.getSelection();
      if (selection) {
        const range = document.createRange();
        range.selectNodeContents(els.artifact);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    }
    window.clearTimeout(copyTimer);
    copyTimer = window.setTimeout(() => { els.copy.textContent = "Copy artifact"; }, 1600);
  });

  function registerWebMCP() {
    const context = navigator.modelContext || document.modelContext;
    if (!context || typeof context.registerTool !== "function") return;
    try {
      const registration = context.registerTool({
        name: "run_relay_demo",
        description: "Replay a simulated RelayReady handoff with recorded local validator output. Does not execute agents, a validator or external actions.",
        inputSchema: {
          type: "object",
          properties: { scenario: { type: "string", enum: [...scenarios.keys()] } },
          required: ["scenario"],
          additionalProperties: false
        },
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        execute: async (input) => {
          if (!input || !scenarios.has(input.scenario)) throw new Error("Unknown RelayReady demo scenario.");
          els.scenario.value = input.scenario;
          resetRelay();
          const result = await runRelay();
          return { content: [{ type: "text", text: JSON.stringify(result) }] };
        }
      });
      Promise.resolve(registration).catch(() => {});
    } catch {
      // Optional browser capability; the visible controls remain available.
    }
  }

  async function loadFixtures() {
    try {
      const response = await fetch("demo-fixtures.json");
      if (!response.ok) throw new Error("Fixture request failed.");
      const data = await response.json();
      if (data.profile !== "0.1-draft" || !Array.isArray(data.scenarios) || !data.scenarios.length) {
        throw new Error("Unexpected fixture format.");
      }
      for (const scenario of data.scenarios) {
        const receipt = scenario.receipt;
        if (typeof scenario.id !== "string" || scenarios.has(scenario.id) ||
            typeof scenario.label !== "string" || typeof scenario.summary !== "string" ||
            typeof scenario.handoff !== "string" || typeof scenario.readback !== "string" ||
            !scenario.checkpoint || !scenario.observation || !receipt ||
            receipt.relayready_receipt !== "0.1-draft" || !Object.hasOwn(decisions, receipt.decision) ||
            !Array.isArray(receipt.reasons) || !receipt.reasons.every((reason) =>
              typeof reason.code === "string" && typeof reason.message === "string")) {
          throw new Error("Incomplete recorded scenario.");
        }
        scenarios.set(scenario.id, scenario);
      }
      els.scenario.replaceChildren(...[...scenarios.values()].map((scenario) => {
        const option = document.createElement("option");
        option.value = scenario.id;
        option.textContent = scenario.label;
        return option;
      }));
      els.scenario.value = scenarios.keys().next().value;
      els.scenario.disabled = false;
      els.reset.disabled = false;
      els.copy.disabled = false;
      resetRelay();
      registerWebMCP();
    } catch {
      scenarios.clear();
      els.summary.textContent = "The recorded scenarios could not be loaded. Reload the page to try again.";
      els.summary.classList.add("load-error");
      els.status.textContent = "UNAVAILABLE";
      els.status.className = "result-escalate";
      els.artifact.textContent = "Recorded artifacts are unavailable. No validation result is shown.";
      els.decisionTitle.textContent = "Demonstration unavailable";
      els.decisionSummary.textContent = "No recorded result could be loaded. The protocol and profile descriptions below remain available.";
    }
  }

  loadFixtures();
})();
