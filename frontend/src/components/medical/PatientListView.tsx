import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Patient } from '@/types/medical';
import { Clock, User, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface PatientListViewProps {
  onPatientSelect: (patient: Patient) => void;
}

const PatientListView: React.FC<PatientListViewProps> = ({ onPatientSelect }) => {
  const navigate = useNavigate();

  // Mock patient data
  const patients: Patient[] = [
    {
      id: 'PT-001',
      name: 'Sarah Johnson',
      age: 45,
      gender: 'Female',
      condition: 'Routine Check-up',
      lastUpdate: '2 hours ago',
      contact: {
        phone: '+1 (555) 123-4567',
        email: 'sarah.johnson@email.com',
        address: '123 Main St, Springfield, IL 62701'
      },
      vitals: {
        bloodPressure: '120/80',
        bloodSugar: 95,
        cholesterol: 180
      },
      lifestyle: {
        smokingStatus: 'Never',
        alcoholConsumption: 'Occasional',
        exerciseFrequency: 'Weekly',
        activityLevel: 'Moderate'
      },
      brainScan: {
        imageUrl: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400',
        hasTumor: false,
        diagnosis: 'Normal brain anatomy, no abnormalities detected',
        mlAnalysis: {
          cancerProbability: 2.1,
          reasoning: 'Brain tissue appears normal with expected gray and white matter distribution'
        },
        scanDate: '2024-06-15'
      }
    },
    {
      id: 'PT-002',
      name: 'Michael Chen',
      age: 52,
      gender: 'Male',
      condition: 'Follow-up Brain Scan',
      lastUpdate: '4 hours ago',
      contact: {
        phone: '+1 (555) 987-6543',
        email: 'michael.chen@email.com',
        address: '456 Oak Ave, Springfield, IL 62702'
      },
      vitals: {
        bloodPressure: '135/85',
        bloodSugar: 110,
        cholesterol: 220
      },
      lifestyle: {
        smokingStatus: 'Former',
        alcoholConsumption: 'Regular',
        exerciseFrequency: 'Rarely',
        activityLevel: 'Light'
      },
      brainScan: {
        imageUrl: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400',
        hasTumor: true,
        diagnosis: 'Small lesion detected in left frontal lobe, requires further evaluation',
        mlAnalysis: {
          cancerProbability: 78.3,
          reasoning: 'Abnormal tissue density and contrast enhancement patterns suggest possible malignancy'
        },
        scanDate: '2024-06-18'
      }
    },
    {
      id: 'PT-003',
      name: 'Emily Rodriguez',
      age: 38,
      gender: 'Female',
      condition: 'Headache Investigation',
      lastUpdate: '1 day ago',
      contact: {
        phone: '+1 (555) 456-7890',
        email: 'emily.rodriguez@email.com',
        address: '789 Pine St, Springfield, IL 62703'
      },
      vitals: {
        bloodPressure: '118/78',
        bloodSugar: 88,
        cholesterol: 165
      },
      lifestyle: {
        smokingStatus: 'Never',
        alcoholConsumption: 'None',
        exerciseFrequency: 'Daily',
        activityLevel: 'Active'
      },
      brainScan: {
        imageUrl: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400',
        hasTumor: false,
        diagnosis: 'No structural abnormalities, likely tension headaches',
        mlAnalysis: {
          cancerProbability: 1.8,
          reasoning: 'Brain structure appears normal with no signs of mass lesions or abnormal enhancement'
        },
        scanDate: '2024-06-17'
      }
    }
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Medical Dashboard</h1>
          <p className="text-gray-600">Patient Management System</p>
        </div>
        <Button
          onClick={() => navigate('/')}
          variant="outline"
          className="flex items-center gap-2"
        >
          <Home className="h-4 w-4" />
          Back to Home
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Patient List ({patients.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {patients.map((patient) => (
              <div
                key={patient.id}
                onClick={() => onPatientSelect(patient)}
                className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <Avatar className="h-12 w-12">
                  <AvatarImage src={patient.avatar} />
                  <AvatarFallback className="bg-blue-100 text-blue-600">
                    {patient.name.split(' ').map(n => n[0]).join('')}
                  </AvatarFallback>
                </Avatar>

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">{patient.name}</h3>
                    <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      {patient.id}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{patient.condition}</p>
                  <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                    <Clock className="h-3 w-3" />
                    Last updated: {patient.lastUpdate}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PatientListView;
