export const PROFILE = "0.1-draft";
export const EVALUATOR = "relayready-browser-workbench/0.1";
export const serialize = value => JSON.stringify(value, null, 2) + "\n";
export const clone = value => JSON.parse(JSON.stringify(value));
const DIGEST = /^sha256:[0-9a-f]{64}$/;
const TEXT = value => typeof value === "string" && /[^\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]/u.test(value);
const validDigest = value => typeof value === "string" && DIGEST.test(value);
export class InputError extends Error {}

export function parseJSON(text) {
  if (typeof text !== "string" || text.length > 2_000_000) throw new InputError("JSON must be smaller than 2 MB.");
  let value;
  try { value = JSON.parse(text); } catch { throw new InputError("Malformed JSON."); }
  // JSON.parse silently accepts duplicate keys. Reject that ambiguity before use.
  const stack = [];
  for (let i = 0; i < text.length; i++) {
    if (text[i] === "{") stack.push(new Set());
    else if (text[i] === "[") stack.push(null);
    else if (text[i] === "}" || text[i] === "]") stack.pop();
    else if (text[i] === '"') {
      const start = i++;
      for (; i < text.length; i++) {
        if (text[i] === "\\") i++;
        else if (text[i] === '"') break;
      }
      let next = i + 1;
      while (/\s/.test(text[next] || "") && next < text.length) next++;
      if (text[next] === ":") {
        const key = JSON.parse(text.slice(start, i + 1));
        const keys = stack[stack.length - 1];
        if (keys?.has(key)) throw new InputError("Duplicate JSON key: " + key);
        keys?.add(key);
      }
    }
  }
  return value;
}

function exact(value, keys, label) {
  if (!value || Array.isArray(value) || typeof value !== "object" ||
      Object.keys(value).length !== keys.length || keys.some(key => !Object.hasOwn(value, key))) {
    throw new InputError(label + " has missing or unexpected fields.");
  }
}
export function timestamp(value) {
  if (typeof value !== "string") throw new InputError("A timestamp is required.");
  const m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]{1,3}))?(Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$/.exec(value);
  if (!m) throw new InputError("Use RFC 3339 time with offset and at most millisecond precision.");
  const [year, month, day, hour, minute, second] = m.slice(1, 7).map(Number);
  const wall = new Date(0);
  wall.setUTCFullYear(year, month - 1, day);
  wall.setUTCHours(hour, minute, second, 0);
  if (year < 1 || month < 1 || month > 12 || day < 1 || hour > 23 || minute > 59 || second > 59 ||
      wall.getUTCFullYear() !== year || wall.getUTCMonth() !== month - 1 || wall.getUTCDate() !== day) {
    throw new InputError("Timestamp contains an invalid calendar date or time.");
  }
  const result = Date.parse(value);
  const utcYear = new Date(result).getUTCFullYear();
  if (!Number.isFinite(result) || utcYear < 1 || utcYear > 9999) throw new InputError("Timestamp is outside the supported UTC year range.");
  return result;
}
export const iso = value => new Date(value).toISOString().replace(".000Z", "Z");
export async function digest(text) {
  const bytes = new TextEncoder().encode(text);
  const hash = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return "sha256:" + [...new Uint8Array(hash)].map(x => x.toString(16).padStart(2, "0")).join("");
}
export function validateObservation(value) {
  exact(value, ["relayready_observation", "checkpoint_sha256", "observed_at", "resources", "effects", "run_inputs"], "Observation");
  if (value.relayready_observation !== PROFILE || !validDigest(value.checkpoint_sha256)) throw new InputError("Unknown observation profile or malformed checkpoint digest.");
  timestamp(value.observed_at);
  for (const [group, key, fields] of [
    ["resources", "id", ["id", "revision"]],
    ["effects", "id", ["id", "status", "evidence"]],
    ["run_inputs", "name", ["name", "digest"]]
  ]) {
    if (!Array.isArray(value[group]) || value[group].length > 1000) throw new InputError(group + " must be an array of at most 1000 entries.");
    const seen = new Set();
    for (const row of value[group]) {
      exact(row, fields, group);
      if (!TEXT(row[key]) || seen.has(row[key])) throw new InputError(group + " contains an empty or duplicate identifier.");
      seen.add(row[key]);
      if (group === "resources" && row.revision !== null && !TEXT(row.revision)) throw new InputError("Resource revision must be nonempty or null.");
      if (group === "run_inputs" && row.digest !== null && !validDigest(row.digest)) throw new InputError("Input digest must be sha256 plus 64 lowercase hexadecimal characters, or null.");
      if (group === "effects" && (!["not_applied", "applied", "unknown"].includes(row.status) ||
          (row.evidence !== null && !TEXT(row.evidence)))) throw new InputError("Effect status or evidence is invalid.");
    }
  }
  return value;
}
const CONTRACT_CODES = new Set(["human_questions_open", "readback_conflicts", "state_needs_recheck", "duplicate_recheck"]);
export async function prepareTemplate(raw) {
  if (!raw || !TEXT(raw.id) || !raw.contract) throw new InputError("Example contract metadata is unavailable.");
  const checkpoint = parseJSON(raw.checkpoint_raw);
  const observation = validateObservation(parseJSON(raw.observation_raw));
  const bindings = {};
  for (const [name, text] of [["handoff", raw.handoff], ["readback", raw.readback], ["checkpoint", raw.checkpoint_raw], ["observation", raw.observation_raw]]) {
    bindings[name + "_sha256"] = await digest(text);
    if (bindings[name + "_sha256"] !== raw.receipt.bindings[name + "_sha256"]) throw new InputError("Recorded example bytes do not match their receipt.");
  }
  if (checkpoint.handoff_sha256 !== bindings.handoff_sha256 || checkpoint.readback_sha256 !== bindings.readback_sha256 ||
      observation.checkpoint_sha256 !== bindings.checkpoint_sha256) throw new InputError("Example binding chain is inconsistent.");
  const times = [raw.contract.handoff_created, raw.contract.readback_created, checkpoint.created, checkpoint.expires_at].map(timestamp);
  if (!(times[0] <= times[1] && times[1] <= times[2] && times[2] < times[3])) throw new InputError("Example chronology is invalid.");
  if (!Array.isArray(raw.contract.findings) || raw.contract.findings.some(x => !CONTRACT_CODES.has(x.code))) throw new InputError("Unsupported example contract finding.");
  return {...raw, checkpoint, observation, bindings};
}

export async function evaluate(template, observationRaw, evaluatedAt) {
  const observed = validateObservation(parseJSON(observationRaw));
  const now = timestamp(evaluatedAt);
  const cp = template.checkpoint;
  const reasons = [];
  let severity = 0;
  function reason(level, code, message, path, action) {
    severity = Math.max(severity, level);
    reasons.push({code, message, path, action});
  }
  if (observed.checkpoint_sha256 !== template.bindings.checkpoint_sha256) {
    reason(2, "checkpoint_digest_mismatch", "Observation is bound to a different checkpoint.", "bindings", "Rebuild observations for the exact issued checkpoint.");
  }
  if (now < timestamp(template.contract.handoff_created)) reason(1, "handoff_in_future", "Handoff creation is after evaluation time.", "clock", "Use a valid evaluation time.");
  if (now < timestamp(template.contract.readback_created)) reason(1, "readback_in_future", "Readback creation is after evaluation time.", "clock", "Use a valid evaluation time.");
  if (now < timestamp(cp.created)) reason(1, "checkpoint_not_active", "Checkpoint creation is after evaluation time.", "clock", "Wait for the checkpoint's validity window.");
  if (now >= timestamp(cp.expires_at)) reason(1, "checkpoint_expired", "Checkpoint has reached its expiry time.", "clock", "Issue a fresh checkpoint and obtain new observations.");
  if (timestamp(observed.observed_at) < timestamp(cp.created)) reason(1, "observation_too_old", "Observation precedes checkpoint creation.", "clock", "Collect a new observation after the checkpoint.");
  if (timestamp(observed.observed_at) > now) reason(1, "observation_in_future", "Observation is after evaluation time.", "clock", "Reconcile the clocks before trusting this record.");
  const rows = [];
  for (const [group, key, field] of [["resources", "id", "revision"], ["run_inputs", "name", "digest"], ["effects", "id", "status"]]) {
    const expected = new Map(cp[group].map(row => [row[key], row]));
    const actual = new Map(observed[group].map(row => [row[key], row]));
    for (const [id, row] of actual) if (!expected.has(id)) {
      reason(2, "unexpected_" + group, "Unexpected " + group + " entry: " + id + ".", group + ":" + id, "Review the observation scope; do not silently add undeclared work.");
      rows.push({group, id, expected: "Not declared", observed: row[field], status: "unexpected"});
    }
    for (const [id, planned] of expected) {
      const current = actual.get(id);
      const path = group + ":" + id;
      let status = "matches";
      if (!current) {
        status = "missing";
        reason(1, "missing_" + group, "Missing " + group + " observation: " + id + ".", path, "Collect the missing observation.");
      } else if (group === "effects") {
        if (current.status !== "not_applied") {
          status = "reconcile";
          reason(2, "effect_requires_reconciliation", "Effect " + id + " is " + current.status + "; do not blindly replay it.", path, "Establish what happened, reconcile the operation and issue a successor before retrying.");
        } else if (!current.evidence) {
          status = "unverified";
          reason(1, "effect_evidence_missing", "Effect " + id + " needs an evidence ref.", path, "Supply a reconciliation evidence reference; the executor must verify its truth.");
        }
      } else if (current[field] === null || current[field] !== planned[field]) {
        status = current[field] === null ? "unknown" : "changed";
        reason(1, group + "_changed", group + " entry " + id + " needs rechecking.", path,
          group === "resources" ? "Re-read the resource and review its revision before continuing." : "Inspect the changed bytes and re-evaluate the pinned input.");
      }
      rows.push({group, id, expected: group === "effects" ? "not_applied + evidence" : planned[field],
        observed: current ? current[field] : "Not supplied", evidence: current?.evidence, status});
    }
  }
  for (const finding of template.contract.findings) {
    reason(finding.code === "state_needs_recheck" ? 1 : 2, finding.code, finding.message, "contract",
      "Resolve the issued handoff/readback condition and issue a successor; observations cannot waive it.");
  }
  const assessment = {
    relayready_browser_assessment: PROFILE, evaluator: EVALUATOR,
    scope: "Supplied prevalidated example contract and edited observations; not full arbitrary-contract validation or execution authority.",
    task_id: cp.task_id, evaluated_at: iso(now), decision: ["resume", "recheck", "escalate"][severity],
    reasons, bindings: {...template.bindings, observation_sha256: await digest(observationRaw)}
  };
  return {assessment, rows};
}

export function makeBundle(template, observationRaw, assessment) {
  return {
    relayready_workbench: PROFILE, template_id: template.id, evaluated_at: assessment.evaluated_at,
    artifacts: {handoff: template.handoff, readback: template.readback, checkpoint: template.checkpoint_raw, observation: observationRaw},
    assessment: clone(assessment),
    reproduction: "relayready gate bundle experiment.json --replay --json",
    warning: "Simulated observations. Replay uses the recorded evaluation clock; it is not permission to resume now."
  };
}
export async function importBundle(text, templates) {
  const bundle = parseJSON(text);
  exact(bundle, ["relayready_workbench", "template_id", "evaluated_at", "artifacts", "assessment", "reproduction", "warning"], "Bundle");
  if (bundle.relayready_workbench !== PROFILE) throw new InputError("Unsupported workbench profile.");
  const template = templates.find(t => t.id === bundle.template_id);
  if (!template) throw new InputError("Unknown example contract. Use the Python CLI for arbitrary handoffs.");
  exact(bundle.artifacts, ["handoff", "readback", "checkpoint", "observation"], "Artifacts");
  for (const [name, source] of [["handoff", "handoff"], ["readback", "readback"], ["checkpoint", "checkpoint_raw"]]) {
    if (bundle.artifacts[name] !== template[source]) throw new InputError("Imported " + name + " is not the exact supported example.");
  }
  const observation = validateObservation(parseJSON(bundle.artifacts.observation));
  if (observation.checkpoint_sha256 !== template.bindings.checkpoint_sha256) {
    throw new InputError("This binding mismatch is outside the editable workbench. Use the Python CLI to inspect it.");
  }
  for (const group of ["resources", "effects", "run_inputs"]) {
    const key = group === "run_inputs" ? "name" : "id";
    if (observation[group].some(row => !template.checkpoint[group].some(expected => expected[key] === row[key]))) {
      throw new InputError("Unexpected observation identifiers cannot be edited here. Use the Python CLI; no fields were discarded.");
    }
  }
  const result = await evaluate(template, bundle.artifacts.observation, bundle.evaluated_at);
  // Imported claims never establish a decision: recompute and compare every field.
  if (serialize(result.assessment) !== serialize(bundle.assessment)) throw new InputError("Imported assessment differs from independent browser recomputation.");
  return {bundle, template, ...result};
}
export function compareBundles(before, after) {
  const rows = [];
  function walk(a, b, path) {
    if (JSON.stringify(a) === JSON.stringify(b)) return;
    if (a && b && typeof a === "object" && typeof b === "object") {
      for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) walk(a[key], b[key], path ? path + "." + key : key);
    } else rows.push({path, before: a === undefined ? "(absent)" : a, after: b === undefined ? "(absent)" : b});
  }
  walk({template: before.template_id, evaluated_at: before.evaluated_at, observation: parseJSON(before.artifacts.observation)},
    {template: after.template_id, evaluated_at: after.evaluated_at, observation: parseJSON(after.artifacts.observation)}, "");
  return {before: before.assessment.decision, after: after.assessment.decision, rows,
    addedReasons: after.assessment.reasons.filter(r => !before.assessment.reasons.some(x => x.code === r.code)).map(r => r.code),
    removedReasons: before.assessment.reasons.filter(r => !after.assessment.reasons.some(x => x.code === r.code)).map(r => r.code)};
}
export function suiteCases(templates) {
  const cases = templates.map(t => ({name: t.label, template: t, observation: clone(t.observation), now: t.receipt.evaluated_at, expected: t.receipt.decision}));
  const clean = templates.find(t => t.id === "clean");
  for (const [name, expected, mutate, now] of [
    ["Expired checkpoint", "recheck", () => {}, clean.checkpoint.expires_at],
    ["Missing resource", "recheck", o => { o.resources = []; }],
    ["Missing reconciliation evidence", "recheck", o => { o.effects[0].evidence = null; }],
    ["Drift + uncertain effect", "escalate", o => { o.resources[0].revision = "new-revision"; o.effects[0].status = "unknown"; }],
    ["Wrong checkpoint binding", "escalate", o => { o.checkpoint_sha256 = "sha256:" + "0".repeat(64); }]
  ]) {
    const observation = clone(clean.observation);
    mutate(observation);
    cases.push({name, expected, template: clean, observation, now: now || clean.receipt.evaluated_at});
  }
  return cases;
}
