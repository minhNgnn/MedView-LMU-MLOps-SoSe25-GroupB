
export interface Patient {
  id: string;
  name: string;
  age: number;
  gender: 'Male' | 'Female' | 'Other';
  condition: string;
  lastUpdate: string;
  avatar?: string;
  contact: {
    phone: string;
    email: string;
    address: string;
  };
  vitals: {
    bloodPressure: string;
    bloodSugar: number;
    cholesterol: number;
  };
  lifestyle: {
    smokingStatus: 'Never' | 'Former' | 'Current';
    alcoholConsumption: 'None' | 'Occasional' | 'Regular' | 'Heavy';
    exerciseFrequency: 'Never' | 'Rarely' | 'Weekly' | 'Daily';
    activityLevel: 'Sedentary' | 'Light' | 'Moderate' | 'Active';
  };
  brainScan: {
    imageUrl: string;
    hasTumor: boolean;
    diagnosis: string;
    mlAnalysis: {
      cancerProbability: number;
      reasoning: string;
    };
    scanDate: string;
  };
}
