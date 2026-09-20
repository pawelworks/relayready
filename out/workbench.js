import {clone, serialize, prepareTemplate, evaluate, makeBundle, importBundle, compareBundles, suiteCases, iso, InputError} from "./workbench-engine.mjs";
const $ = id => document.getElementById(id);
const state = {templates: [], template: null, runs: [], nextRun: 1, revision: 0, current: null, suite: null};
const labels = {resources:"Resource revisions",run_inputs:"Pinned input bytes",effects:"Previous operation"};
const messages = {
  resume:"The declared example contract and supplied observations are consistent at this clock. This is not permission to execute.",
  recheck:"Some observations are missing, changed or outside the validity window. Collect fresh evidence before relying on this checkpoint.",
  escalate:"An unresolved question, binding or previous effect needs a decision. Do not blindly retry the work."
};
function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function announce(text) { $("announcement").textContent = text; }
function fieldLabel(text, id) {
  const label = node("label", text);
  label.htmlFor = id;
  return label;
}
function input(id, value, label, parent) {
  parent.append(fieldLabel(label, id));
  const field = node("input");
  field.id = id; field.type = "text"; field.value = value ?? "";
  field.maxLength = 300; field.autocomplete = "off"; field.spellcheck = false;
  parent.append(field);
  return field;
}
function markStale() {
  state.revision++;
  state.current = null;
  $("exportBundle").disabled = true;
  $("resultState").textContent = "DRAFT CHANGED";
  const panel = document.querySelector(".decision-panel");
  panel.dataset.stale = "true"; delete panel.dataset.decision;
  $("decision").textContent = "Needs evaluation";
  $("decisionMark").textContent = "↻";
  $("decisionSummary").textContent = "Your draft changed. Evaluate again; an earlier decision does not apply to these inputs.";
  $("reasonList").replaceChildren();
  $("resultMeta").textContent = "No current assessment. Earlier runs remain unchanged in the notebook.";
  $("evidenceRows").replaceChildren(node("p", "Evaluate the edited draft to compare this evidence.", "muted"));
  renderArtifact();
}
function toControl(value) { return iso(Date.parse(value)).replace("Z",""); }
function fromControl(id) {
  const raw = $(id).value;
  if (!raw) throw new InputError("Both observation and evaluation times are required.");
  return raw + (raw.split("T")[1].length === 5 ? ":00Z" : "Z");
}
function loadDraft(template, observation = template.observation, now = template.receipt.evaluated_at) {
  state.template = template;
  $("template").value = template.id;
  $("templateSummary").textContent = template.summary;
  const container = $("observationFields");
  container.replaceChildren();
  for (const group of ["resources","run_inputs","effects"]) {
    const fieldset = node("fieldset");
    fieldset.append(node("legend",labels[group]));
    template.checkpoint[group].forEach((expected,index) => {
      const key = group === "run_inputs" ? "name" : "id";
      const current = observation[group].find(row => row[key] === expected[key]);
      const base = group + "-" + index;
      const box = node("div",undefined,"field-group");
      box.append(node("p",expected[key],"field-id"));
      const includeLabel = node("label",undefined,"row-label");
      const include = node("input");
      include.type="checkbox"; include.id=base+"-included"; include.checked=Boolean(current);
      includeLabel.append(include,document.createTextNode("Observation supplied"));
      box.append(includeLabel);
      if (group === "effects") {
        box.append(fieldLabel("Previous outcome",base+"-status"));
        const select=node("select"); select.id=base+"-status";
        for (const [value,label] of [["not_applied","Not applied"],["applied","Already applied"],["unknown","Unknown outcome"]]) {
          const option=node("option",label); option.value=value; select.append(option);
        }
        select.value=current?.status || "unknown"; box.append(select);
        input(base+"-evidence",current?.evidence,"Evidence reference",box);
      } else {
        const field = group === "resources" ? "revision" : "digest";
        input(base+"-value",current?.[field],group === "resources" ? "Observed revision" : "Observed SHA-256",box);
        box.append(node("p","Leave blank for unknown. Uncheck to test a missing observation.","field-id"));
      }
      fieldset.append(box);
    });
    container.append(fieldset);
  }
  $("observedAt").value = toControl(observation.observed_at);
  $("evaluatedAt").value = toControl(now);
  markStale();
}
function observationFromForm() {
  const observation={relayready_observation:"0.1-draft",checkpoint_sha256:state.template.bindings.checkpoint_sha256,
    observed_at:fromControl("observedAt"),resources:[],effects:[],run_inputs:[]};
  for (const group of ["resources","run_inputs","effects"]) {
    state.template.checkpoint[group].forEach((expected,index) => {
      const base=group+"-"+index;
      if (!$(base+"-included").checked) return;
      if (group === "effects") {
        observation[group].push({id:expected.id,status:$(base+"-status").value,evidence:$(base+"-evidence").value || null});
      } else {
        const key=group==="resources"?"id":"name", field=group==="resources"?"revision":"digest";
        observation[group].push({[key]:expected[key],[field]:$(base+"-value").value || null});
      }
    });
  }
  return observation;
}
function renderEvidence(rows) {
  const container=$("evidenceRows"); container.replaceChildren();
  for (const [index,row] of rows.entries()) {
    const line=node("div",undefined,"evidence-row"); line.id="evidence-"+index; line.dataset.status=row.status;
    const identity=node("div"); identity.append(node("small",labels[row.group]),node("strong",row.id),node("span",row.status,"status"));
    const expected=node("div"); expected.append(node("small","EXPECTED"),node("code",row.expected));
    const observed=node("div"); observed.append(node("small","OBSERVED"),node("code",row.observed ?? "Unknown"));
    if (row.evidence) observed.append(node("small","Evidence: "+row.evidence));
    line.append(identity,expected,observed); container.append(line);
  }
}
function showResult(run) {
  state.current=run;
  const {assessment,rows}=run, panel=document.querySelector(".decision-panel");
  panel.dataset.decision=assessment.decision; panel.dataset.stale="false";
  $("resultState").textContent="FRESH BROWSER CHECK";
  $("decision").textContent=assessment.decision[0].toUpperCase()+assessment.decision.slice(1);
  $("decisionMark").textContent={resume:"✓",recheck:"↻",escalate:"!"}[assessment.decision];
  $("decisionSummary").textContent=messages[assessment.decision];
  $("reasonList").replaceChildren();
  for (const reason of assessment.reasons) {
    const link=node("a",undefined,"reason");
    const rowIndex=rows.findIndex(row => row.group+":"+row.id===reason.path);
    link.href=rowIndex>=0?"#evidence-"+rowIndex:reason.path==="clock"?"#observedAt":"#artifactsHeading";
    link.append(node("strong",reason.message),node("span",reason.action),node("code",reason.code));
    $("reasonList").append(link);
  }
  $("resultMeta").textContent="Evaluated "+assessment.evaluated_at+" · "+assessment.evaluator+" · "+assessment.reasons.length+" reason(s). Full arbitrary-contract checks remain in the CLI.";
  $("exportBundle").disabled=false;
  renderEvidence(rows); renderArtifact();
  announce(assessment.decision+". "+assessment.reasons.length+" reasons. Fresh local sandbox result.");
}
function addRun(template,observationRaw,result,provenance="Browser evaluation") {
  const run={id:state.nextRun++,label:template.label,templateId:template.id,provenance,
    ...clone(result),bundle:makeBundle(template,observationRaw,result.assessment)};
  state.runs.push(run); if(state.runs.length>20)state.runs.shift();
  renderHistory(); showResult(run);
  return run;
}
async function evaluateDraft() {
  const revision=state.revision, template=state.template;
  $("evaluate").disabled=true;
  try {
    const raw=serialize(observationFromForm()), now=fromControl("evaluatedAt");
    const result=await evaluate(template,raw,now);
    if(revision!==state.revision)return;
    addRun(template,raw,result);
  } catch(error) {
    if(revision!==state.revision)return;
    state.current=null; $("exportBundle").disabled=true;
    const panel=document.querySelector(".decision-panel"); panel.dataset.decision="error"; panel.dataset.stale="false";
    $("resultState").textContent="INPUT ERROR"; $("decision").textContent="Check the input"; $("decisionMark").textContent="!";
    $("decisionSummary").textContent=error.message; $("reasonList").replaceChildren();
    $("resultMeta").textContent="No continuation decision was issued.";
    announce("Input error. "+error.message);
  } finally { $("evaluate").disabled=false; }
}
function renderArtifact() {
  if(!state.template)return;
  const choice=$("artifactChoice").value;
  let text;
  if(choice==="assessment")text=state.current?serialize(state.current.assessment):"No current assessment. Evaluate this draft.";
  else if(state.current)text=state.current.bundle.artifacts[choice];
  else if(choice==="observation") {
    try{text=serialize(observationFromForm());}catch{text="Complete the observation fields to inspect this draft.";}
  }else text=state.template[choice==="checkpoint"?"checkpoint_raw":choice];
  $("artifactText").textContent=text;
}
function renderHistory() {
  const list=$("runList"); list.replaceChildren();
  $("runCount").textContent=state.runs.length+" saved in this tab · maximum 20";
  for(const run of [...state.runs].reverse()) {
    const card=node("article",undefined,"run-card");
    card.append(node("strong","#"+run.id+" · "+run.assessment.decision),node("small",run.label),node("small",run.assessment.evaluated_at));
    const restore=node("button","Duplicate as draft","small-button"); restore.type="button";
    restore.addEventListener("click",()=>{
      const template=state.templates.find(t=>t.id===run.templateId);
      loadDraft(template,JSON.parse(run.bundle.artifacts.observation),run.assessment.evaluated_at);
      $("inputs-title").scrollIntoView({block:"start"}); $("template").focus();
    });
    const download=node("button","Export this run","small-button"); download.type="button";
    download.addEventListener("click",()=>downloadJSON(run.bundle,"relayready-run-"+run.id+".json"));
    card.append(restore,download); list.append(card);
  }
  for(const id of ["baselineRun","candidateRun"]) {
    const select=$(id), prior=select.value;
    select.replaceChildren();
    for(const run of state.runs){const option=node("option","#"+run.id+" "+run.label+" · "+run.assessment.decision);option.value=String(run.id);select.append(option);}
    select.disabled=state.runs.length<2;
    if(id==="candidateRun")select.value=String(state.runs.at(-1)?.id);
    else if(state.runs.some(r=>String(r.id)===prior))select.value=prior;
  }
  renderComparison();
}
function renderComparison() {
  const container=$("comparison");container.replaceChildren();
  if(state.runs.length<2){container.append(node("p","Evaluate twice to compare decisions and evidence.","muted"));return;}
  const before=state.runs.find(r=>String(r.id)===$("baselineRun").value);
  const after=state.runs.find(r=>String(r.id)===$("candidateRun").value);
  const diff=compareBundles(before.bundle,after.bundle);
  container.append(node("h3",diff.before+" → "+diff.after));
  container.append(node("p","Added reasons: "+(diff.addedReasons.join(", ")||"none")+". Removed: "+(diff.removedReasons.join(", ")||"none")+".","muted"));
  if(!diff.rows.length)container.append(node("p","No changed inputs. The evaluator is deterministic for the same inputs and clock.","muted"));
  for(const row of diff.rows){
    const line=node("div",undefined,"diff-row");
    const format=value=>typeof value==="object"?JSON.stringify(value):String(value);
    line.append(node("code",row.path),node("del",format(row.before)),node("ins",format(row.after)));container.append(line);
  }
}
function downloadJSON(value,filename) {
  const url=URL.createObjectURL(new Blob([serialize(value)],{type:"application/json"}));
  const link=node("a");link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function runSuite() {
  $("runSuite").disabled=true; $("suiteResults").textContent="Evaluating declared local cases…";
  const results=[];
  try {
    for(const item of suiteCases(state.templates)){
      const raw=serialize(item.observation), result=await evaluate(item.template,raw,item.now);
      results.push({name:item.name,expected:item.expected,actual:result.assessment.decision,
        passed:result.assessment.decision===item.expected,bundle:makeBundle(item.template,raw,result.assessment)});
    }
    state.suite={relayready_contract_suite:"0.1-draft",scope:"Simulated local contract cases; not a model benchmark.",results};
    const container=$("suiteResults");container.replaceChildren();
    const count=results.filter(r=>r.passed).length;
    container.append(node("p",count+" / "+results.length+" cases matched expected decisions."));
    const grid=node("div",undefined,"suite-grid");
    for(const item of results){
      const card=node("div",undefined,"suite-case"), copy=node("div");
      copy.append(node("strong",item.name),node("small","Expected "+item.expected+" · observed "+item.actual));
      card.append(copy,node("span",item.passed?"PASS":"FAIL",item.passed?"suite-pass":"suite-fail"));grid.append(card);
    }
    const exportButton=node("button","Export suite evidence","small-button");
    exportButton.addEventListener("click",()=>downloadJSON(state.suite,"relayready-contract-suite.json"));
    container.append(grid,exportButton);announce(count+" of "+results.length+" local cases passed.");
  }catch(error){$("suiteResults").textContent="Suite did not complete: "+error.message;}
  finally{$("runSuite").disabled=false;}
}
$("experimentForm").addEventListener("submit",event=>{event.preventDefault();evaluateDraft();});
$("experimentForm").addEventListener("input",markStale);
$("template").addEventListener("change",()=>loadDraft(state.templates.find(t=>t.id===$("template").value)));
$("reset").addEventListener("click",()=>loadDraft(state.template));
$("artifactChoice").addEventListener("change",renderArtifact);
$("baselineRun").addEventListener("change",renderComparison);
$("candidateRun").addEventListener("change",renderComparison);
$("exportBundle").addEventListener("click",()=>{if(state.current)downloadJSON(state.current.bundle,"relayready-experiment.json");});
$("runSuite").addEventListener("click",runSuite);
$("importBundle").addEventListener("change",async()=>{
  const file=$("importBundle").files[0];if(!file)return;
  const revision=++state.revision;
  $("importStatus").textContent="Checking the supplied bundle locally…";
  try{
    if(file.size>2_000_000)throw new InputError("The file exceeds the 2 MB limit.");
    const imported=await importBundle(await file.text(),state.templates);
    if(revision!==state.revision){$("importStatus").textContent="Import ignored because the draft changed during verification.";return;}
    loadDraft(imported.template,JSON.parse(imported.bundle.artifacts.observation),imported.bundle.evaluated_at);
    addRun(imported.template,imported.bundle.artifacts.observation,imported,"Imported, independently recomputed");
    $("importStatus").textContent="Input hashes and assessment independently reproduced. No file was uploaded.";
  }catch(error){$("importStatus").textContent="Import rejected: "+error.message;}
  finally{$("importBundle").value="";}
});
async function init(){
  try{
    const response=await fetch("./demo-fixtures.json");
    if(!response.ok)throw new Error("The example bundle could not be loaded.");
    const data=await response.json();
    state.templates=await Promise.all(data.scenarios.map(prepareTemplate));
    $("template").replaceChildren();
    for(const template of state.templates){const option=node("option",template.label);option.value=template.id;$("template").append(option);}
    for(const id of ["template","evaluate","reset","runSuite"])$(id).disabled=false;
    loadDraft(state.templates[0]);await evaluateDraft();
  }catch(error){
    $("fatalError").hidden=false;$("fatalError").textContent="Workbench unavailable: "+error.message;
    $("decision").textContent="Examples unavailable";$("decisionSummary").textContent="No continuation decision can be issued. Reload once the example files are available.";
  }
}
init();
