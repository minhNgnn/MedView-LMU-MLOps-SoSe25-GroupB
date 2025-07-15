import React, { useState } from "react";
import { Button } from "./ui/button";

const MonitoringDashboard: React.FC = () => {
  const [reportPath, setReportPath] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateDriftReport = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/monitoring/drift-report?days=7");
      if (!response.ok) throw new Error("Failed to generate drift report");
      const data = await response.json();
      setReportPath(data.report_path);
    } catch (err) {
      alert("Error generating drift report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", minHeight: "100vh", justifyContent: "flex-start" }}>
      <h1 style={{ textAlign: "center", marginTop: "2rem" }}>
        Brain Tumor Image Monitoring Dashboard
      </h1>
      <Button
        onClick={generateDriftReport}
        disabled={loading}
        style={{ margin: "1.5rem 0", alignSelf: "center" }}
      >
        {loading ? "Generating..." : "Generate Drift Report"}
      </Button>
      {reportPath && (
        <iframe
          title="Drift Report"
          src={`http://localhost:8000/monitoring/report/${reportPath.split("/").pop()}`}
          style={{ width: "90vw", height: "80vh", border: "1px solid #ccc", marginTop: "2rem" }}
        />
      )}
    </div>
  );
};

export default MonitoringDashboard;
