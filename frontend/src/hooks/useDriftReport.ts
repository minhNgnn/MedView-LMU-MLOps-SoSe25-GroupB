import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export function useDriftReport() {
  const [loading, setLoading] = useState(false);
  const [reportPath, setReportPath] = useState<string | null>(null);

  const generateDriftReport = async (days: number = 7) => {
    setLoading(true);
    setReportPath(null);
    try {
      const response = await fetch(`${API_BASE_URL}/monitoring/drift-report?days=${days}`);
      if (!response.ok) throw new Error('Failed to generate drift report');
      const data = await response.json();
      setReportPath(data.report_path);
    } catch (err) {
      setReportPath(null);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { generateDriftReport, loading, reportPath };
}
