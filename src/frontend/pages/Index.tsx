import { useState } from "react";
import PatientForm from "@/components/PatientForm";
import PredictionResults from "@/components/PredictionResults";
import RecentPatients from "@/components/RecentPatients";
import { PatientData, PredictionResult } from "@/types/health";

const Index = () => {
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePrediction = async (patientData: PatientData) => {
    setIsLoading(true);
    
    try {
      // Simulate API call to your local ML backend
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate network delay

      const response = await fetch('/predict', { // Assuming your backend is accessible at /predict
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: PredictionResult = await response.json();
      setPredictionResult(result);

    } catch (error) {
      console.error('Prediction API error:', error);
      // Optionally, you can set a user-friendly error message here
      // For now, it will just log the error to the console.

      // Fallback to a generic mock result if API call fails
      setPredictionResult({
        heartDiseaseRisk: 50,
        diabetesRisk: 50,
        confidence: 70,
        recommendations: [
          "Data could not be processed by the ML model. Please check the backend service.",
          "Ensure all fields are correctly filled."
        ]
      });

    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-slate-900">Smart Health Risk Assistant</h1>
          <p className="text-sm text-slate-600 mt-1">AI-powered health risk prediction for general practitioners</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Patient Form - Takes up 2 columns on large screens */}
          <div className="lg:col-span-2">
            <PatientForm onSubmit={handlePrediction} isLoading={isLoading} />
          </div>

          {/* Results Section - Takes up 1 column on large screens */}
          <div className="lg:col-span-1">
            <PredictionResults result={predictionResult} isLoading={isLoading} />
          </div>

          {/* Recent Patients - Takes up 1 column on large screens */}
          <div className="lg:col-span-1">
            <RecentPatients />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
