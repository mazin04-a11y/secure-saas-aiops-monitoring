import React from "react";
import ReactDOM from "react-dom/client";
import { Activity, AlertTriangle, Brain, ServerCog } from "lucide-react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./styles.css";

type Metric = {
  id: number;
  service_name: string;
  cpu_usage: number;
  memory_usage: number;
  response_time_ms: number;
  error_rate: number;
  status: string;
  created_at: string;
};

type Incident = {
  id: number;
  incident_type: string;
  severity: string;
  status: string;
  evidence: string;
  recommendation: string;
  created_at: string;
  source_label: string;
  correlation_id: string;
};

type AccessLog = {
  id: number;
  user_id: number;
  action: string;
  ip_address: string;
  outcome: string;
  created_at: string;
};

type AgentTaskLog = {
  id: number;
  agent_name: string;
  task_name: string;
  permission_scope: string;
  guardrail_status: string;
  evidence: string;
  recommendation: string;
  created_at: string;
  source_label: string;
  correlation_id: string;
};

type ExternalIntelReport = {
  id: number;
  query: string;
  source: string;
  status: string;
  summary: string;
  evidence: string;
  created_at: string;
};

type ExternalIntelStatus = {
  connected: boolean;
  status: string;
  latest_summary: string | null;
};

type AgentAssessment = {
  mode: string;
  summary: string;
  tools_used: string[];
  incidents_created: number;
  recommendations: string[];
  guardrail_status: string;
  prompt_feedback: string;
};

const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const navItems = [
  { id: "overview", label: "Overview" },
  { id: "metrics", label: "Performance" },
  { id: "security", label: "Security" },
  { id: "incidents", label: "Incidents" },
  { id: "agents", label: "Agents" },
  { id: "intel", label: "External Intel" },
  { id: "evidence", label: "Evidence" },
];

function App() {
  const [metrics, setMetrics] = React.useState<Metric[]>([]);
  const [accessLogs, setAccessLogs] = React.useState<AccessLog[]>([]);
  const [incidents, setIncidents] = React.useState<Incident[]>([]);
  const [agentLogs, setAgentLogs] = React.useState<AgentTaskLog[]>([]);
  const [intelReports, setIntelReports] = React.useState<ExternalIntelReport[]>([]);
  const [intelStatus, setIntelStatus] = React.useState<ExternalIntelStatus | null>(null);
  const [intelFeedback, setIntelFeedback] = React.useState("");
  const [assessment, setAssessment] = React.useState<AgentAssessment | null>(null);
  const [missionPrompt, setMissionPrompt] = React.useState("");
  const [intelQuery, setIntelQuery] = React.useState("");
  const [activeSection, setActiveSection] = React.useState(() => {
    const hash = window.location.hash.replace("#", "");
    return navItems.some((item) => item.id === hash) ? hash : "overview";
  });
  const [loading, setLoading] = React.useState(false);

  const loadData = React.useCallback(async () => {
    const [
      metricsResponse,
      accessLogsResponse,
      incidentsResponse,
      agentLogsResponse,
      intelReportsResponse,
      intelStatusResponse,
    ] = await Promise.all([
      fetch(`${apiBase}/metrics`),
      fetch(`${apiBase}/access-logs`),
      fetch(`${apiBase}/incidents`),
      fetch(`${apiBase}/agent-logs`),
      fetch(`${apiBase}/external-intel`),
      fetch(`${apiBase}/external-intel/status`),
    ]);
    setMetrics(await metricsResponse.json());
    setAccessLogs(await accessLogsResponse.json());
    setIncidents(await incidentsResponse.json());
    setAgentLogs(await agentLogsResponse.json());
    setIntelReports(await intelReportsResponse.json());
    setIntelStatus(await intelStatusResponse.json());
  }, []);

  React.useEffect(() => {
    loadData().catch(console.error);
  }, [loadData]);

  function navigateToSection(sectionId: string) {
    window.history.replaceState(null, "", `#${sectionId}`);
    setActiveSection(sectionId);
  }

  async function runAssessment() {
    setLoading(true);
    try {
      const endpoint = missionPrompt.trim() ? `${apiBase}/agents/prompt` : `${apiBase}/agents/kickoff`;
      const response = await fetch(endpoint, {
        method: "POST",
        headers: missionPrompt.trim() ? { "Content-Type": "application/json" } : undefined,
        body: missionPrompt.trim() ? JSON.stringify({ prompt: missionPrompt }) : undefined,
      });
      setAssessment(await response.json());
      await loadData();
    } finally {
      setLoading(false);
    }
  }

  async function runExternalIntelSearch() {
    if (!intelQuery.trim()) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${apiBase}/external-intel/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: intelQuery }),
      });
      const report = (await response.json()) as ExternalIntelReport;
      setIntelFeedback(report.summary);
      await loadData();
    } finally {
      setLoading(false);
    }
  }

  const latest = metrics[0];
  const hasInternalData = metrics.length > 0 || accessLogs.length > 0;
  const failedLogins = accessLogs.filter((log) => log.outcome === "failed").length;
  const highIncidents = incidents.filter((incident) => incident.severity === "high").length;
  const systemStatus = !hasInternalData
    ? "No Data"
    : highIncidents > 0 || failedLogins >= 3
      ? "Critical"
      : incidents.length > 0
        ? "Warning"
        : "Healthy";
  const topRisk =
    (incidents[0] ? displayEvidence(incidents[0].evidence) : undefined) ??
    (latest ? `${latest.service_name} currently reports ${latest.status} status.` : "No live data source connected.");
  const nextAction =
    incidents[0]?.recommendation ??
    (hasInternalData
      ? "Run a live assessment against the ingested operational data."
      : "Connect a service or send data to /metrics/ingest and /access-logs/ingest.");
  const chartData = [...metrics].reverse().map((metric) => ({
    name: formatTime(metric.created_at),
    cpu: metric.cpu_usage,
    memory: metric.memory_usage,
    response: metric.response_time_ms,
  }));

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <ServerCog size={28} />
          <div>
            <strong>SaaS AIOps</strong>
            <span>Project 4 Template</span>
          </div>
        </div>
        <nav>
          {navItems.map((item) => (
            <button
              className={activeSection === item.id ? "active" : ""}
              key={item.id}
              onClick={() => navigateToSection(item.id)}
              type="button"
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <section className="content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Secure SaaS Application with Integrated AIOps Monitoring</p>
            <h1>Operational health command center</h1>
          </div>
          <button onClick={runAssessment} disabled={loading || !hasInternalData}>
            <Brain size={18} />
            {loading ? "Running agents" : hasInternalData ? "Run AIOps crew" : "Waiting for Data"}
          </button>
        </header>

        {activeSection === "overview" ? (
          <section className="page">
            <div className="metrics-grid">
              <Kpi icon={<ServerCog />} label="System Status" value={systemStatus} />
              <Kpi icon={<ServerCog />} label="Live Data Source" value={hasInternalData ? "Receiving" : "Not Connected"} />
              <Kpi icon={<ServerCog />} label="External Intel" value={intelStatus?.connected ? "Connected" : "Not Connected"} />
              <Kpi icon={<Activity />} label="Latest CPU" value={latest ? `${latest.cpu_usage}%` : "--"} />
            </div>
            <section className="decision-grid">
              <article className="panel">
                <div className="panel-heading">
                  <h2>Top Operational Risk</h2>
                  <span>{systemStatus}</span>
                </div>
                <p>{topRisk}</p>
              </article>
              <article className="panel">
                <div className="panel-heading">
                  <h2>Recommended Next Action</h2>
                  <span>Operator guidance</span>
                </div>
                <p>{nextAction}</p>
              </article>
            </section>
            <section className="panel">
              <div className="panel-heading">
                <h2>Latest External Signal</h2>
                <span>{intelStatus?.status ?? "unknown"}</span>
              </div>
              <p>{intelStatus?.latest_summary ?? "No successful external intelligence report has been collected yet."}</p>
            </section>
            <section className="panel">
              <div className="panel-heading">
                <h2>Recent Agent Activity</h2>
                <span>{agentLogs.length} evidence logs</span>
              </div>
              <button onClick={runAssessment} disabled={loading || !hasInternalData} type="button">
                <Brain size={18} />
                {hasInternalData ? "Run Live Assessment" : "Waiting for Data"}
              </button>
              {agentLogs.slice(0, 3).map((log) => (
                <article className="compact-log" key={log.id}>
                  <strong>{log.agent_name}</strong>
                  <span>{displayEvidence(log.evidence)}</span>
                  <small>{log.source_label} / {formatDateTime(log.created_at)} / {log.correlation_id}</small>
                </article>
              ))}
              {agentLogs.length === 0 ? <p className="empty">Run an assessment to generate agent evidence.</p> : null}
            </section>
          </section>
        ) : null}

        {activeSection === "metrics" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>Application Performance Monitoring</h2>
              <span>CPU, memory, and response time evidence</span>
            </div>
            <div className="chart">
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cpu" stroke="#2563eb" strokeWidth={2} />
                  <Line type="monotone" dataKey="memory" stroke="#16a34a" strokeWidth={2} />
                  <Line type="monotone" dataKey="response" stroke="#dc2626" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="table metadata-table">
              <div className="table-row metric-row table-head">
                <span>Source</span>
                <span>Service</span>
                <span>Status</span>
                <span>Observed</span>
              </div>
              {metrics.map((metric) => (
                <div className="table-row metric-row" key={metric.id}>
                  <span>internal_metrics</span>
                  <span>{metric.service_name}</span>
                  <span>{metric.status}</span>
                  <span>{formatDateTime(metric.created_at)}</span>
                </div>
              ))}
              {metrics.length === 0 ? <p className="empty table-empty">No internal performance metrics received.</p> : null}
            </div>
          </section>
        ) : null}

        {activeSection === "security" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>Security Events</h2>
              <span>Access log evidence for failed logins and sensitive actions</span>
            </div>
            <div className="table">
              <div className="table-row table-head">
                <span>Source</span>
                <span>Action</span>
                <span>IP Address</span>
                <span>Outcome</span>
                <span>Observed</span>
              </div>
              {accessLogs.map((log) => (
                <div className="table-row" key={log.id}>
                  <span>access_logs</span>
                  <span>{log.action}</span>
                  <span>{log.ip_address}</span>
                  <span className={log.outcome === "failed" ? "danger" : "success"}>{log.outcome}</span>
                  <span>{formatDateTime(log.created_at)}</span>
                </div>
              ))}
              {accessLogs.length === 0 ? <p className="empty table-empty">No internal access logs received.</p> : null}
            </div>
          </section>
        ) : null}

        {activeSection === "incidents" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>Incident Register</h2>
              <span>Business-readable evidence and recommendations</span>
            </div>
            <div className="incident-list">
              {incidents.map((incident) => (
                <article key={incident.id} className="incident">
                  <div>
                    <strong>{incident.incident_type}</strong>
                    <span>{displayEvidence(incident.evidence)}</span>
                  </div>
                  <p>{incident.recommendation}</p>
                  <small>
                    {incident.severity} severity / {incident.status} / {incident.source_label} / {formatDateTime(incident.created_at)}
                  </small>
                  <small>Correlation ID: {incident.correlation_id}</small>
                </article>
              ))}
              {incidents.length === 0 ? <p className="empty">No internal incidents have been created.</p> : null}
            </div>
          </section>
        ) : null}

        {activeSection === "agents" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>Agent Assessment</h2>
              <span>Visible decision evidence without exposing hidden reasoning</span>
            </div>
            <div className="prompt-box">
              <label htmlFor="missionPrompt">Mission prompt</label>
              <textarea
                id="missionPrompt"
                maxLength={500}
                placeholder="Focus on response time, failed login patterns, or current operational risk."
                value={missionPrompt}
                onChange={(event) => setMissionPrompt(event.target.value)}
              />
              <small>{missionPrompt.length}/500 characters / guarded assessment only</small>
            </div>
            {assessment ? (
              <div className="assessment">
                <p>{assessment.summary}</p>
                <span className={`guardrail ${assessment.guardrail_status}`}>
                  Guardrail {assessment.guardrail_status}: {assessment.prompt_feedback}
                </span>
                <strong>Tools used: {assessment.tools_used.join(", ")}</strong>
                <ul>
                  {assessment.recommendations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="empty">Run the AIOps crew to generate assessment evidence.</p>
            )}
          </section>
        ) : null}

        {activeSection === "intel" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>External Intelligence</h2>
              <span>Public search intelligence with safeguards</span>
            </div>
            <div className="prompt-box">
              <label htmlFor="intelQuery">Search query</label>
              <textarea
                id="intelQuery"
                maxLength={240}
                placeholder="Search public status or operational intelligence, e.g. payment provider outage status."
                value={intelQuery}
                onChange={(event) => setIntelQuery(event.target.value)}
              />
              <small>{intelQuery.length}/240 characters / no secrets, credentials, or exploit queries</small>
            </div>
            <button onClick={runExternalIntelSearch} disabled={loading || !intelQuery.trim()} type="button">
              Search External Intel
            </button>
            {intelStatus ? (
              <span className={`guardrail ${intelStatus.connected ? "accepted" : "rejected"}`}>
                External Intel {intelStatus.status}
              </span>
            ) : null}
            {intelFeedback ? <p className="empty">{intelFeedback}</p> : null}
            <div className="incident-list">
              {intelReports.map((report) => (
                <article className="incident" key={report.id}>
                  <div>
                    <strong>{report.query}</strong>
                    <span>{report.status}</span>
                  </div>
                  <p>{report.summary}</p>
                  <small>{report.source} / context only / {formatDateTime(report.created_at)}</small>
                </article>
              ))}
              {intelReports.length === 0 ? <p className="empty">No external intelligence reports yet.</p> : null}
            </div>
          </section>
        ) : null}

        {activeSection === "evidence" ? (
          <section className="panel page">
            <div className="panel-heading">
              <h2>Agent Reports</h2>
              <span>Identity-aware task logs and permission evidence</span>
            </div>
            <div className="incident-list">
              {agentLogs.map((log) => (
                <article className="incident" key={log.id}>
                  <div>
                    <strong>{log.agent_name} / {log.task_name}</strong>
                    <span>{log.guardrail_status}</span>
                  </div>
                  <p>{displayEvidence(log.evidence)}</p>
                  <small>{log.source_label} / {formatDateTime(log.created_at)} / {log.permission_scope}</small>
                  <small>Correlation ID: {log.correlation_id}</small>
                  <small>{log.recommendation}</small>
                </article>
              ))}
              {agentLogs.length === 0 ? <p className="empty">Run the AIOps crew to create agent evidence logs.</p> : null}
            </div>
          </section>
        ) : null}

      </section>
    </main>
  );
}

function Kpi({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <article className="kpi">
      <span>{icon}</span>
      <p>{label}</p>
      <strong>{value}</strong>
    </article>
  );
}

function formatDateTime(value?: string | null) {
  if (!value) {
    return "No timestamp";
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function formatTime(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function displayEvidence(value: string) {
  return value.replace(/\[source: [^\]]+\]\s*/g, "").replace(/\[correlation: [^\]]+\]\s*/g, "");
}

ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
