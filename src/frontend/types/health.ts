
export interface PatientData {
  age: number;
  gender: 'male' | 'female' | 'other';
  bloodPressure: number;
  bloodSugar: number;
  cholesterol: number;
  smoker: boolean;
}

export interface PredictionResult {
  heartDiseaseRisk: number;
  diabetesRisk: number;
  confidence: number;
  recommendations: string[];
}

export interface PatientRecord {
  id: string;
  name: string;
  age: number;
  gender: string;
  lastVisit: string;
  riskLevel: 'low' | 'medium' | 'high';
}
