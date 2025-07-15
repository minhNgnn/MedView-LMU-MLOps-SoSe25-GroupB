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
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Brain Tumor Image Monitoring Dashboard</h1>
        <Button onClick={generateDriftReport} disabled={loading}>
          Generate Drift Report
        </Button>
      </div>
      {reportPath && (
        <iframe
          src={`http://localhost:8000/monitoring/report/${reportPath.split("/").pop()}`}
          width="100%"
          height="900px"
          style={{ border: "none" }}
          title="Evidently Drift Report"
        />
      )}
    </div>
  );
};

export default MonitoringDashboard;
