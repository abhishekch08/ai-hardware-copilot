"use strict";

const dom = {
  sidebar: document.querySelector("#sidebar"),
  scrim: document.querySelector("#sidebarScrim"),
  thread: document.querySelector("#thread"),
  empty: document.querySelector("#emptyState"),
  form: document.querySelector("#ideaForm"),
  idea: document.querySelector("#ideaInput"),
  title: document.querySelector("#ideaTitle"),
  requirements: document.querySelector("#requirements"),
  constraints: document.querySelector("#constraints"),
  risk: document.querySelector("#riskTier"),
  rounds: document.querySelector("#rounds"),
  submit: document.querySelector("#submitIdea"),
  runTitle: document.querySelector("#runTitle"),
  modeBadge: document.querySelector("#modeBadge"),
  providerLabel: document.querySelector("#providerLabel"),
  modeNotice: document.querySelector("#modeNotice"),
  statusDot: document.querySelector("#statusDot"),
  history: document.querySelector("#historyList"),
  dialog: document.querySelector("#connectionDialog"),
  connectionForm: document.querySelector("#connectionForm"),
  token: document.querySelector("#tokenInput"),
  connectionError: document.querySelector("#connectionError"),
};

const app = {
  token: "",
  config: null,
  currentJobId: null,
  currentConferenceId: null,
  pollGeneration: 0,
  history: [],
};

function element(tag, className, text) {
  const value = document.createElement(tag);
  if (className) value.className = className;
  if (text !== undefined && text !== null) value.textContent = String(text);
  return value;
}

function lines(value) {
  return String(value || "").split("\n").map((item) => item.trim()).filter(Boolean);
}

function uid() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

function initializeToken() {
  const fragment = new URLSearchParams(location.hash.slice(1));
  const supplied = fragment.get("token");
  if (supplied) {
    sessionStorage.setItem("copilot-token", supplied);
    history.replaceState(null, "", `${location.pathname}${location.search}`);
  }
  app.token = supplied || sessionStorage.getItem("copilot-token") || "";
}

async function api(path, options = {}) {
  if (!app.token) throw new Error("Local access token is required.");
  const headers = new Headers(options.headers || {});
  headers.set("Authorization", `Bearer ${app.token}`);
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { ...options, headers });
  const body = await response.json().catch(() => ({ error: "The runtime returned an unreadable response." }));
  if (response.status === 401) {
    showConnection("The token was rejected. Use the current token from the local command.");
    throw new Error("Unauthorized");
  }
  if (!response.ok) throw new Error(body.error || `Request failed with status ${response.status}`);
  return body;
}

function showConnection(message = "") {
  dom.connectionError.textContent = message;
  dom.token.value = app.token;
  if (!dom.dialog.open) dom.dialog.showModal();
  requestAnimationFrame(() => dom.token.focus());
}

async function connect(event) {
  event.preventDefault();
  const token = dom.token.value.trim();
  if (!token) return;
  app.token = token;
  try {
    await loadConfiguration();
    sessionStorage.setItem("copilot-token", token);
    dom.connectionError.textContent = "";
    dom.dialog.close();
    await loadHistory();
  } catch (error) {
    dom.connectionError.textContent = error.message;
  }
}

async function loadConfiguration() {
  const config = await api("/v1/config");
  app.config = config;
  const live = Boolean(config.reasoning_enabled);
  dom.providerLabel.textContent = live ? "Reasoning connected" : "Dry-run safeguards";
  dom.modeNotice.textContent = config.mode_notice;
  dom.statusDot.className = `status-dot ${live ? "live" : "dry"}`;
  dom.modeBadge.className = `mode-badge ${live ? "live" : "dry"}`;
  dom.modeBadge.textContent = live ? "Live reasoning" : "Dry run";
  return config;
}

async function loadHistory() {
  const value = await api("/v1/jobs?limit=60");
  app.history = value.jobs.filter((job) => ["idea_conference", "conference"].includes(job.operation));
  renderHistory();
  return app.history;
}

function renderHistory() {
  dom.history.replaceChildren();
  if (!app.history.length) {
    dom.history.append(element("p", "history-empty", "No conferences yet"));
    return;
  }
  for (const job of app.history) {
    const button = element("button", "history-item");
    button.type = "button";
    if (job.conference_id === app.currentConferenceId || job.job_id === app.currentJobId) {
      button.classList.add("active");
    }
    button.append(element("span", "history-title", job.title));
    const meta = element("span", "history-meta");
    meta.append(
      element("span", "", formatDate(job.created_at)),
      element("span", "", formatJobStatus(job.status)),
    );
    button.append(meta);
    button.addEventListener("click", () => openHistoryJob(job));
    dom.history.append(button);
  }
}

async function openHistoryJob(job) {
  closeSidebar();
  if (job.conference_id) {
    await loadConference(job.conference_id);
    return;
  }
  if (job.status === "queued" || job.status === "running") {
    clearThread();
    app.currentJobId = job.job_id;
    renderUserMessage(job.title);
    const shell = createAssistantShell(job.title, "Conference in progress");
    dom.thread.append(shell.root);
    await pollJob(job.job_id, shell);
    return;
  }
  clearThread();
  const shell = createAssistantShell(job.title, "Conference could not be opened");
  showError(shell, job.error || "No conference result is available.");
  dom.thread.append(shell.root);
}

function clearThread() {
  app.pollGeneration += 1;
  app.currentJobId = null;
  app.currentConferenceId = null;
  dom.thread.replaceChildren();
}

function newConference() {
  clearThread();
  dom.thread.append(dom.empty);
  dom.empty.hidden = false;
  dom.runTitle.textContent = "New engineering conference";
  dom.form.reset();
  dom.risk.value = "T2";
  dom.rounds.value = "3";
  dom.submit.disabled = false;
  resizeComposer();
  renderHistory();
  closeSidebar();
  dom.idea.focus();
}

function renderUserMessage(text) {
  const wrapper = element("article", "message");
  wrapper.append(element("div", "message-label", "You"));
  wrapper.append(element("div", "user-message", text));
  dom.thread.append(wrapper);
}

function createAssistantShell(title, subtitle) {
  const root = element("article", "message assistant-message");
  const heading = element("div", "result-heading");
  const copy = element("div");
  copy.append(element("h2", "", title || "Engineering conference"));
  copy.append(element("p", "", subtitle || "Preparing the specialist review"));
  const state = element("div", "job-state");
  state.append(element("span", "spinner"), element("span", "job-state-label", "Queued"));
  heading.append(copy, state);
  const body = element("div", "progress-body");
  root.append(heading, body);
  return { root, heading, state, body, copy };
}

function buildIdeaPayload(overrides = {}) {
  const idea = String(overrides.idea ?? dom.idea.value).trim();
  if (idea.length < 20) throw new Error("Describe the idea in at least 20 characters.");
  const id = uid();
  return {
    task_id: overrides.task_id || `web-${Date.now().toString(36)}-${id.slice(0, 8)}`,
    title: String(overrides.title ?? dom.title.value).trim(),
    idea,
    risk_tier: overrides.risk_tier || dom.risk.value,
    iterate_rounds: Number(overrides.iterate_rounds ?? dom.rounds.value),
    requirements: overrides.requirements || lines(dom.requirements.value),
    constraints: overrides.constraints || lines(dom.constraints.value),
  };
}

async function submitIdea(event, overrides) {
  if (event) event.preventDefault();
  if (!app.token) {
    showConnection();
    return null;
  }
  let payload;
  try {
    payload = buildIdeaPayload(overrides || {});
  } catch (error) {
    dom.idea.setCustomValidity(error.message);
    dom.idea.reportValidity();
    dom.idea.setCustomValidity("");
    return null;
  }

  clearThread();
  dom.empty.hidden = true;
  dom.runTitle.textContent = payload.title || "Engineering conference";
  renderUserMessage(payload.idea);
  const shell = createAssistantShell(payload.title || "Engineering conference", "Screening the specialist network");
  dom.thread.append(shell.root);
  dom.submit.disabled = true;
  dom.thread.scrollTop = dom.thread.scrollHeight;
  renderProgress(shell, "queued");

  try {
    const key = uid();
    const job = await api("/v1/jobs", {
      method: "POST",
      headers: { "Idempotency-Key": key },
      body: JSON.stringify({ operation: "idea_conference", payload }),
    });
    app.currentJobId = job.job_id;
    app.currentConferenceId = `CONF-${payload.task_id}`;
    await loadHistory();
    const completed = await pollJob(job.job_id, shell);
    return completed || job;
  } catch (error) {
    showError(shell, error.message);
    return null;
  } finally {
    dom.submit.disabled = false;
  }
}

async function pollJob(jobId, shell) {
  const generation = ++app.pollGeneration;
  while (generation === app.pollGeneration) {
    const job = await api(`/v1/jobs/${encodeURIComponent(jobId)}`);
    renderProgress(shell, job.status);
    if (job.status === "succeeded") {
      app.currentConferenceId = job.result.conference_id;
      const view = await api(`/v1/conferences/${encodeURIComponent(job.result.conference_id)}`);
      renderConference(shell, view);
      await loadHistory();
      renderHistory();
      return job;
    }
    if (job.status === "failed") {
      showError(shell, job.error || "The conference failed.");
      await loadHistory();
      return job;
    }
    if (app.currentConferenceId) {
      try {
        const partial = await api(`/v1/conferences/${encodeURIComponent(app.currentConferenceId)}`);
        renderProgress(shell, job.status, partial.state);
      } catch (error) {
        if (!String(error.message).includes("not found")) console.warn(error);
      }
    }
    await delay(900);
  }
  return null;
}

function renderProgress(shell, jobStatus, conferenceState = "") {
  const label = shell.state.querySelector(".job-state-label");
  if (label) label.textContent = formatJobStatus(jobStatus);
  shell.body.replaceChildren();
  shell.body.append(element("p", "", statusDescription(jobStatus, conferenceState)));
  const phases = [
    ["Freeze the product brief", 0],
    ["Screen all 184 specialists", 1],
    ["Collect independent positions", 2],
    ["Resolve objections and iterate", 3],
    ["Evaluate convergence gates", 4],
  ];
  const current = phaseIndex(jobStatus, conferenceState);
  const list = element("div", "phase-list");
  for (const [name, index] of phases) {
    const item = element("div", `phase-item ${index < current ? "done" : index === current ? "active" : ""}`);
    item.append(
      element("span", "phase-index", index < current ? "✓" : index + 1),
      element("span", "", name),
    );
    list.append(item);
  }
  shell.body.append(list);
}

function phaseIndex(jobStatus, state) {
  if (jobStatus === "queued") return 0;
  if (jobStatus === "succeeded" || jobStatus === "failed") return 4;
  const values = {
    INTAKE: 0,
    CONTEXT_FROZEN: 1,
    ALL_AGENTS_SCREENED: 1,
    WORK_CELL_FORMED: 2,
    INDEPENDENT_ANALYSIS: 2,
    POSITIONS_COLLECTED: 3,
    OBJECTIONS_OPEN: 3,
    PROPOSAL_REVISED: 3,
    AFFECTED_AGENTS_REACTIVATED: 3,
    OBJECTIONS_RESOLVED: 4,
    VERIFIED: 4,
    FINALIZED: 4,
    BLOCKED: 4,
  };
  return values[state] ?? 1;
}

function statusDescription(jobStatus, state) {
  if (jobStatus === "queued") return "The request is queued on the local worker.";
  if (jobStatus === "running") {
    return state ? `Current conference state: ${formatState(state)}.` : "The conference is running. Large specialist cells can take time.";
  }
  if (jobStatus === "failed") return "The runtime stopped without producing an engineering decision.";
  return "The conference finished and its audit record is available.";
}

function renderConference(shell, view) {
  shell.root.classList.add("complete");
  shell.state.replaceChildren(element("span", `badge ${stateClass(view.state)}`, formatState(view.state)));
  shell.copy.querySelector("p").textContent = `${view.agents_screened} screened · ${view.active_agents.length} active · proposal v${view.proposal_version}`;
  shell.body.remove();

  const content = element("div", "result-content");
  if (view.provider === "dry-run") {
    content.append(element(
      "div",
      "notice",
      "This is an orchestration check. The dry-run provider intentionally reports insufficient evidence and does not perform real specialist engineering analysis.",
    ));
  }

  const tabs = [
    ["summary", "Summary"],
    ["specialists", `Specialists (${view.positions.length})`],
    ["objections", `Objections (${view.objections.filter((item) => item.status !== "resolved").length})`],
    ["audit", "Audit"],
  ];
  const tabList = element("div", "tab-list");
  tabList.setAttribute("role", "tablist");
  const panels = element("div");
  tabs.forEach(([id, label], index) => {
    const button = element("button", `tab-button ${index === 0 ? "active" : ""}`, label);
    button.type = "button";
    button.setAttribute("role", "tab");
    button.setAttribute("aria-selected", index === 0 ? "true" : "false");
    button.dataset.tab = id;
    const panel = element("section", "tab-panel");
    panel.dataset.panel = id;
    panel.hidden = index !== 0;
    if (id === "summary") buildSummary(panel, view);
    if (id === "specialists") buildSpecialists(panel, view.positions);
    if (id === "objections") buildObjections(panel, view.objections);
    if (id === "audit") buildAudit(panel, view);
    tabList.append(button);
    panels.append(panel);
  });
  tabList.addEventListener("click", (event) => {
    const target = event.target.closest("[data-tab]");
    if (!target) return;
    for (const button of tabList.querySelectorAll("[data-tab]")) {
      const selected = button === target;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-selected", String(selected));
    }
    for (const panel of panels.querySelectorAll("[data-panel]")) {
      panel.hidden = panel.dataset.panel !== target.dataset.tab;
    }
  });
  content.append(tabList, panels);
  shell.root.append(content);
  dom.runTitle.textContent = view.task.title;
  dom.thread.scrollTop = dom.thread.scrollHeight;
}

function buildSummary(panel, view) {
  const openObjections = view.objections.filter((item) => item.status !== "resolved").length;
  const metrics = element("div", "metrics-grid");
  [
    [view.agents_screened, "Agents screened"],
    [view.active_agents.length, "Active specialists"],
    [view.current_round, "Rounds completed"],
    [openObjections, "Open objections"],
  ].forEach(([value, label]) => {
    const card = element("div", "metric");
    card.append(element("strong", "", value), element("span", "", label));
    metrics.append(card);
  });
  panel.append(metrics);
  panel.append(element("h3", "section-title", "Objective"));
  panel.append(element("p", "summary-text", view.task.objective));
  panel.append(element("h3", "section-title", "Specialist coverage"));
  panel.append(buildBreakdown(view.attendance_counts, view.agents_screened));
  panel.append(element("h3", "section-title", "Current verdicts"));
  panel.append(buildBreakdown(view.verdict_counts, Math.max(1, view.positions.length)));

  const workCell = element("details", "agent-card");
  const summary = element("summary", "agent-summary");
  summary.append(element("strong", "", `Active work cell · ${view.active_agents.length} specialists`));
  workCell.append(summary);
  const body = element("div", "agent-body");
  const list = element("ul", "compact-list");
  view.active_agents.forEach((agent) => {
    list.append(element("li", "", `${agent.agent_id} — ${agent.agent_name}${agent.mandatory ? " · mandatory" : ""}`));
  });
  body.append(list);
  workCell.append(body);
  panel.append(element("h3", "section-title", "Work cell"), workCell);

  panel.append(element("h3", "section-title", "Coverage and release gates"));
  const coverage = view.coverage_report;
  if (!coverage) {
    panel.append(element("p", "summary-text", "Coverage has not yet been evaluated."));
  } else if (coverage.passed) {
    panel.append(element("p", "summary-text", "All configured convergence checks passed."));
  } else {
    const list = element("ul", "coverage-list");
    (coverage.failures || []).forEach((failure) => list.append(element("li", "", failure)));
    panel.append(list);
  }
}

function buildBreakdown(values, total) {
  const root = element("div", "breakdown");
  const entries = Object.entries(values || {});
  if (!entries.length) {
    root.append(element("p", "summary-text", "No results yet."));
    return root;
  }
  for (const [name, count] of entries) {
    const row = element("div", "metric-row");
    row.append(element("span", "", humanize(name)));
    const track = element("progress", "bar-track");
    track.max = Math.max(1, total);
    track.value = Number(count);
    track.setAttribute("aria-label", `${humanize(name)}: ${count} of ${total}`);
    row.append(track, element("output", "", count));
    root.append(row);
  }
  return root;
}

function buildSpecialists(panel, positions) {
  if (!positions.length) {
    panel.append(element("p", "summary-text", "No specialist positions are available."));
    return;
  }
  const filter = element("input", "filter-input");
  filter.type = "search";
  filter.placeholder = "Filter by agent, verdict, risk or rationale";
  filter.setAttribute("aria-label", "Filter specialist positions");
  const list = element("div", "agent-list");
  const sorted = [...positions].sort((a, b) => a.agent_id.localeCompare(b.agent_id));
  sorted.forEach((position) => {
    const card = element("details", "agent-card");
    card.dataset.search = JSON.stringify(position).toLowerCase();
    const summary = element("summary", "agent-summary");
    const identity = element("span", "agent-identity");
    identity.append(
      element("strong", "", position.agent_name),
      element("span", "", `${position.agent_id} · ${Math.round(position.confidence * 100)}% confidence`),
    );
    summary.append(identity, element("span", `badge ${position.verdict}`, humanize(position.verdict)));
    const body = element("div", "agent-body");
    body.append(element("p", "", position.rationale || "No rationale returned."));
    appendListSection(body, "Risks", position.risks);
    appendListSection(body, "Assumptions", position.assumptions);
    appendListSection(body, "Conditions", position.conditions);
    appendListSection(body, "Verification", position.verification);
    if (position.claims?.length) {
      appendListSection(body, "Claims", position.claims.map((claim) => {
        if (typeof claim === "string") return claim;
        return claim.statement || claim.claim || JSON.stringify(claim);
      }));
    }
    card.append(summary, body);
    list.append(card);
  });
  filter.addEventListener("input", () => {
    const query = filter.value.trim().toLowerCase();
    for (const card of list.children) card.hidden = Boolean(query) && !card.dataset.search.includes(query);
  });
  panel.append(filter, list);
}

function appendListSection(root, title, values) {
  if (!values?.length) return;
  root.append(element("h4", "", title));
  const list = element("ul", "compact-list");
  values.forEach((value) => list.append(element("li", "", value)));
  root.append(list);
}

function buildObjections(panel, objections) {
  if (!objections.length) {
    panel.append(element("p", "summary-text", "No objections were recorded for this proposal version."));
    return;
  }
  const list = element("div", "objection-list");
  const order = { critical: 0, major: 1, minor: 2 };
  [...objections].sort((a, b) => (order[a.severity] ?? 3) - (order[b.severity] ?? 3)).forEach((item) => {
    const card = element("article", `objection-card ${item.severity}`);
    const heading = element("div", "agent-summary");
    const identity = element("span", "agent-identity");
    identity.append(
      element("h3", "", `${item.agent_id} — ${item.agent_name}`),
      element("span", "", `${item.objection_id} · ${humanize(item.status)}`),
    );
    heading.append(identity, element("span", `badge ${item.severity}`, item.severity));
    card.append(
      heading,
      element("p", "", item.disputed_claim),
      element("p", "", `Required resolution: ${item.required_resolution}`),
    );
    list.append(card);
  });
  panel.append(list);
}

function buildAudit(panel, view) {
  const actionRow = element("div", "result-heading");
  const copy = element("div");
  copy.append(element("h2", "", "Conference audit"), element("p", "", `${view.events.length} state transitions recorded`));
  const download = element("button", "download-button", "Download report");
  download.type = "button";
  download.addEventListener("click", () => downloadReport(view));
  actionRow.append(copy, download);
  panel.append(actionRow);
  const events = element("div", "audit-events");
  view.events.forEach((event) => {
    const row = element("div", "audit-event");
    row.append(
      element("span", "", `#${event.sequence} · v${event.proposal_version}`),
      element("strong", "", event.actor),
      element("span", "", humanize(event.event_type)),
    );
    events.append(row);
  });
  panel.append(events);
  panel.append(element("h3", "section-title", "Raw report"));
  panel.append(element("pre", "raw-report", view.report_markdown || "Report not generated yet."));
}

function downloadReport(view) {
  const blob = new Blob([view.report_markdown || ""], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${view.conference_id}.md`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function showError(shell, message) {
  shell.state.replaceChildren(element("span", "badge object", "Failed"));
  shell.body.replaceChildren(element("div", "error-panel", message));
}

async function loadConference(conferenceId) {
  app.pollGeneration += 1;
  const view = await api(`/v1/conferences/${encodeURIComponent(conferenceId)}`);
  clearThread();
  app.currentConferenceId = conferenceId;
  dom.runTitle.textContent = view.task.title;
  renderUserMessage(view.task.description);
  const shell = createAssistantShell(view.task.title, "Loading conference record");
  dom.thread.append(shell.root);
  renderConference(shell, view);
  renderHistory();
}

function resizeComposer() {
  dom.idea.style.height = "auto";
  dom.idea.style.height = `${Math.min(dom.idea.scrollHeight, 208)}px`;
}

function closeSidebar() {
  dom.sidebar.classList.remove("open");
  dom.scrim.classList.remove("open");
}

function openSidebar() {
  dom.sidebar.classList.add("open");
  dom.scrim.classList.add("open");
}

function humanize(value) {
  return String(value || "").replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatState(value) {
  const labels = {
    OBJECTIONS_OPEN: "Objections open",
    OBJECTIONS_RESOLVED: "Objections resolved",
    FINALIZED: "Finalized",
    BLOCKED: "Blocked",
    VERIFIED: "Verified",
  };
  return labels[value] || humanize(value);
}

function stateClass(value) {
  if (["FINALIZED", "VERIFIED"].includes(value)) return "approve";
  if (["BLOCKED"].includes(value)) return "object";
  return "approve_with_conditions";
}

function formatJobStatus(value) {
  return { queued: "Queued", running: "Running", succeeded: "Complete", failed: "Failed" }[value] || humanize(value);
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" }).format(date);
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function registerWebMcp() {
  const context = document.modelContext;
  if (!context?.registerTool) return;
  const lifecycle = new AbortController();
  const reportError = (error) => console.warn("WebMCP registration failed", error);
  try {
    void Promise.resolve(context.registerTool({
      name: "start_engineering_conference",
      title: "Start engineering conference",
      description: "Submit a product idea to the visible Lab Copilot workspace and start exhaustive specialist screening and deliberation.",
      inputSchema: {
        type: "object",
        properties: {
          idea: { type: "string", minLength: 20, maxLength: 100000 },
          title: { type: "string", maxLength: 160 },
          risk_tier: { enum: ["T1", "T2"] },
          iterate_rounds: { type: "integer", minimum: 0, maximum: 10 },
          requirements: { type: "array", items: { type: "string" }, maxItems: 100 },
          constraints: { type: "array", items: { type: "string" }, maxItems: 100 },
        },
        required: ["idea"],
        additionalProperties: false,
      },
      annotations: { readOnlyHint: false, untrustedContentHint: true },
      async execute(input) {
        if (!input || typeof input.idea !== "string" || input.idea.trim().length < 20) {
          throw new Error("A product idea of at least 20 characters is required.");
        }
        const job = await submitIdea(null, input);
        return job ? { job_id: job.job_id, status: job.status } : { status: "not_started" };
      },
    }, { signal: lifecycle.signal })).catch(reportError);
    void Promise.resolve(context.registerTool({
      name: "list_engineering_conferences",
      title: "List engineering conferences",
      description: "List recent conference runs visible in the local Lab Copilot workspace.",
      inputSchema: { type: "object", properties: {}, additionalProperties: false },
      annotations: { readOnlyHint: true, untrustedContentHint: false },
      async execute() {
        const jobs = await loadHistory();
        return { conferences: jobs.map(({ job_id, title, status, conference_id, created_at }) => ({
          job_id, title, status, conference_id, created_at,
        })) };
      },
    }, { signal: lifecycle.signal })).catch(reportError);
  } catch (error) {
    reportError(error);
  }
}

document.querySelector("#newConference").addEventListener("click", newConference);
document.querySelector("#refreshHistory").addEventListener("click", () => loadHistory().catch(console.warn));
document.querySelector("#openSidebar").addEventListener("click", openSidebar);
document.querySelector("#closeSidebar").addEventListener("click", closeSidebar);
dom.scrim.addEventListener("click", closeSidebar);
document.querySelector("#changeToken").addEventListener("click", () => showConnection());
dom.connectionForm.addEventListener("submit", connect);
dom.form.addEventListener("submit", submitIdea);
dom.idea.addEventListener("input", resizeComposer);
dom.idea.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    dom.form.requestSubmit();
  }
});
document.querySelectorAll(".example-prompt").forEach((button) => {
  button.addEventListener("click", () => {
    dom.idea.value = button.dataset.prompt;
    resizeComposer();
    dom.idea.focus();
  });
});

async function start() {
  initializeToken();
  resizeComposer();
  registerWebMcp();
  if (!app.token) {
    showConnection();
    return;
  }
  try {
    await loadConfiguration();
    await loadHistory();
  } catch (error) {
    dom.statusDot.className = "status-dot error";
    dom.providerLabel.textContent = "Connection unavailable";
    dom.modeNotice.textContent = error.message;
  }
}

void start();
