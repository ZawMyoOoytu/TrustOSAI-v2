import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Executions.css";

const decisionTypes = [
  "ALL",
  "ALLOW",
  "ALLOW_WITH_MONITORING",
  "REVIEW",
  "BLOCK",
];

export default function Executions() {
  const navigate = useNavigate();

  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("ALL");

  // =====================================================
  // Load Executions
  // =====================================================

  const loadExecutions = async () => {
    try {
      setLoading(true);

      const response = await fetch(
        "http://localhost:8000/executions/"
      );

      if (!response.ok) {
        throw new Error("Cannot load executions");
      }

      const data = await response.json();
      setExecutions(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExecutions();
  }, []);

  // =====================================================
  // Delete Execution
  // =====================================================

  const deleteExecution = async (executionId) => {
    const confirmed = window.confirm(
      `Delete execution #${executionId}?`
    );

    if (!confirmed) return;

    try {
      const response = await fetch(
        `http://localhost:8000/executions/${executionId}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to delete execution");
      }

      await loadExecutions();
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };

  // =====================================================
  // Filter Executions
  // =====================================================

  const filtered = executions.filter((item) => {
    const matchSearch = (item.task || "")
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchFilter =
      filter === "ALL" || item.decision === filter;

    return matchSearch && matchFilter;
  });

  // =====================================================
  // Loading
  // =====================================================

  if (loading) {
    return (
      <div className="executions-page">
        <h2>Loading executions...</h2>
      </div>
    );
  }

  // =====================================================
  // Error
  // =====================================================

  if (error) {
    return (
      <div className="executions-page">
        <h2>❌ {error}</h2>
      </div>
    );
  }

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="executions-page">

      <div className="page-header">
        <h1>⚡ Execution History</h1>
        <p>AI Governance Runtime Telemetry</p>
      </div>

      {/* ===================================== */}
      {/* Search & Filters */}
      {/* ===================================== */}

      <div className="toolbar">

        <input
          type="text"
          placeholder="Search executions..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="filters">
          {decisionTypes.map((status) => (
            <button
              key={status}
              className={
                filter === status ? "active-filter" : ""
              }
              onClick={() => setFilter(status)}
            >
              {status}
            </button>
          ))}
        </div>

      </div>

      {/* ===================================== */}
      {/* Execution Table */}
      {/* ===================================== */}

      <div className="execution-table">

        <div className="table-header">
          <span>ID</span>
          <span>Task</span>
          <span>Agent</span>
          <span>Trust</span>
          <span>Decision</span>
          <span>Created</span>
          <span>Actions</span>
        </div>

        {filtered.length === 0 ? (

          <div className="table-row empty">
            <span>No executions found.</span>
          </div>

        ) : (

          filtered.map((item) => (

            <div
              className="table-row"
              key={item.execution_id}
            >

              <span>
                #{item.execution_id}
              </span>

              <span className="task">
                {item.task || "-"}
              </span>

              <span>
                {item.agent}
              </span>

              <span className="trust">
                {Math.round(item.trust_score)}
              </span>

              <span>
                <DecisionBadge
                  decision={item.decision}
                />
              </span>

              <span>
                {new Date(
                  item.created_at
                ).toLocaleString()}
              </span>

              <span className="actions">

                <button
                  className="view-btn"
                  onClick={() =>
                    navigate(
                      `/executions/${item.execution_id}`
                    )
                  }
                >
                  👁 View
                </button>

                <button
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteExecution(item.execution_id);
                  }}
                >
                  🗑 Delete
                </button>

              </span>

            </div>

          ))

        )}

      </div>

    </div>
  );
}

// =====================================================
// Decision Badge
// =====================================================

function DecisionBadge({ decision }) {

  const badgeClass = decision
    ? decision.toLowerCase().replace(/_/g, "-")
    : "";

  return (
    <span className={`badge ${badgeClass}`}>
      {decision}
    </span>
  );
}