import React from "react";
import { Button } from "./ui/button";
import { useDriftReport } from "../hooks/useDriftReport";

const MonitoringDashboard: React.FC = () => {
  const { generateDriftReport, loading, reportPath } = useDriftReport();

  // Helper to determine iframe src
  const getIframeSrc = () => {
    if (!reportPath) return undefined;
    // If reportPath is a full URL (starts with http), use it directly
    if (/^https?:\/\//.test(reportPath)) {
      return reportPath;
    }
    // Otherwise, assume it's a backend-relative path
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    return `${API_BASE_URL}/monitoring/report/${reportPath.split("/").pop()}`;
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", minHeight: "100vh", justifyContent: "flex-start" }}>
      <h1 style={{ textAlign: "center", marginTop: "2rem" }}>
        Brain Tumor Image Monitoring Dashboard
      </h1>
      <Button
        onClick={() => generateDriftReport(7)}
        disabled={loading}
        style={{ margin: "1.5rem 0", alignSelf: "center" }}
      >
        {loading ? "Generating..." : "Generate Drift Report"}
      </Button>
      {reportPath && (
        <iframe
          title="Drift Report"
          src={getIframeSrc()}
          style={{ width: "90vw", height: "80vh", border: "1px solid #ccc", marginTop: "2rem" }}
        />
      )}
    </div>
  );
};

export default MonitoringDashboard;
