import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Progress } from './ui/progress';

interface DashboardData {
  total_predictions_today: number;
  average_confidence: number;
  most_common_class: string;
  avg_tumor_confidence: number;
  malignant_count: number;
  benign_count: number;
  normal_count: number;
  last_drift_check: string;
  alerts: Array<{
    type: string;
    severity: string;
    message: string;
  }>;
}

interface DataQualityResults {
  data_quality: boolean;
  missing_values_test: boolean;
  outliers_test: boolean;
  drift_test: boolean;
  timestamp: string;
}

const MonitoringDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [dataQualityResults, setDataQualityResults] = useState<DataQualityResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [latestReportPath, setLatestReportPath] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/monitoring/dashboard');
      if (!response.ok) throw new Error('Failed to fetch dashboard data');
      const data = await response.json();
      setDashboardData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const runDataQualityTests = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/monitoring/data-quality');
      if (!response.ok) throw new Error('Failed to run data quality tests');
      const data = await response.json();
      setDataQualityResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const generateDriftReport = async () => {
    try {
      setLoading(true);
      setLatestReportPath(null); // Reset before new request
      const response = await fetch('http://localhost:8000/monitoring/drift-report?days=7');
      if (!response.ok) throw new Error('Failed to generate drift report');
      const data = await response.json();
      setLatestReportPath(data.report_path);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getClassColor = (className: string) => {
    switch (className.toLowerCase()) {
      case 'malignant': return 'bg-red-100 text-red-800';
      case 'benign': return 'bg-yellow-100 text-yellow-800';
      case 'normal': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading brain tumor monitoring data...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Brain Tumor Image Monitoring Dashboard</h1>
        <div className="space-x-2">
          <Button onClick={runDataQualityTests} disabled={loading}>
            Run Image Quality Tests
          </Button>
          <Button onClick={generateDriftReport} disabled={loading}>
            Generate Drift Report
          </Button>
          {latestReportPath && (
            <a
              href={`http://localhost:8000/monitoring/report/${latestReportPath.split('/').pop()}`}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Open Latest Drift Report
            </a>
          )}
        </div>
      </div>

      {error && (
        <Alert>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Today's Predictions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardData?.total_predictions_today || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardData?.average_confidence ? 
                `${(dashboardData.average_confidence * 100).toFixed(1)}%` : 
                'N/A'
              }
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tumor Detection Confidence</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardData?.avg_tumor_confidence ? 
                `${(dashboardData.avg_tumor_confidence * 100).toFixed(1)}%` : 
                'N/A'
              }
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Most Common Class</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardData?.most_common_class || 'N/A'}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tumor Classification Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Brain Tumor Classification Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-red-600">
                {dashboardData?.malignant_count || 0}
              </div>
              <div className="text-sm text-gray-500">Malignant</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-600">
                {dashboardData?.benign_count || 0}
              </div>
              <div className="text-sm text-gray-500">Benign</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {dashboardData?.normal_count || 0}
              </div>
              <div className="text-sm text-gray-500">Normal</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Data Quality Results */}
      {dataQualityResults && (
        <Card>
          <CardHeader>
            <CardTitle>Brain Tumor Image Quality Test Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span>Overall Image Quality</span>
                <Badge variant={dataQualityResults.data_quality ? "default" : "destructive"}>
                  {dataQualityResults.data_quality ? "PASS" : "FAIL"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Missing Values Test</span>
                <Badge variant={dataQualityResults.missing_values_test ? "default" : "destructive"}>
                  {dataQualityResults.missing_values_test ? "PASS" : "FAIL"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Outliers Test</span>
                <Badge variant={dataQualityResults.outliers_test ? "default" : "destructive"}>
                  {dataQualityResults.outliers_test ? "PASS" : "FAIL"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Image Drift Test</span>
                <Badge variant={dataQualityResults.drift_test ? "default" : "destructive"}>
                  {dataQualityResults.drift_test ? "PASS" : "FAIL"}
                </Badge>
              </div>
              <div className="text-sm text-gray-500">
                Last updated: {new Date(dataQualityResults.timestamp).toLocaleString()}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Alerts */}
      {dashboardData?.alerts && dashboardData.alerts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Active Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {dashboardData.alerts.map((alert, index) => (
                <Alert key={index}>
                  <AlertDescription>
                    <div className="flex items-center space-x-2">
                      <Badge className={getSeverityColor(alert.severity)}>
                        {alert.severity.toUpperCase()}
                      </Badge>
                      <span className="font-medium">{alert.type}</span>
                    </div>
                    <p className="mt-1">{alert.message}</p>
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Last Drift Check */}
      {dashboardData?.last_drift_check && (
        <Card>
          <CardHeader>
            <CardTitle>Last Drift Check</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-gray-500">
              {new Date(dashboardData.last_drift_check).toLocaleString()}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default MonitoringDashboard; 