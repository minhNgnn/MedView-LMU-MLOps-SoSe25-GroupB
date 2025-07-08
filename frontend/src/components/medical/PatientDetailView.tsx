import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { ArrowLeft, Home, Phone, Mail, MapPin, Heart, Activity, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  age: number;
  gender: string;
  phone_number: string;
  email: string;
  address: string;
  blood_pressure: string;
  blood_sugar: number;
  cholesterol: number;
  smoking_status: string;
  alcohol_consumption: string;
  exercise_frequency: string;
  activity_level: string;
}

interface PatientDetailViewProps {
  patient: Patient;
  onBack: () => void;
}

const PatientDetailView = ({ patient, onBack }: PatientDetailViewProps) => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Avatar className="h-10 w-10">
                <AvatarFallback className="bg-blue-100 text-blue-700">
                  {patient.first_name[0]}{patient.last_name[0]}
                </AvatarFallback>
              </Avatar>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{patient.first_name} {patient.last_name}</h1>
                <p className="text-sm text-gray-500">ID: {patient.id}</p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleGoHome}
                className="flex items-center space-x-2"
              >
                <Home className="h-4 w-4" />
                <span>Home</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={onBack}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Patient List</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Basic Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <div className="w-2 h-6 bg-blue-500 rounded"></div>
                <span>Basic Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Age</label>
                  <p className="text-sm text-gray-900">{patient.age} years</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Gender</label>
                  <p className="text-sm text-gray-900">{patient.gender}</p>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Address</label>
                <Badge variant="secondary" className="mt-1">
                  {patient.address}
                </Badge>
              </div>
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm">
                  <Phone className="h-4 w-4 text-gray-400" />
                  <span>{patient.phone_number}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Mail className="h-4 w-4 text-gray-400" />
                  <span>{patient.email}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <MapPin className="h-4 w-4 text-gray-400" />
                  <span>{patient.address}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Vitals & Measurements */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <div className="w-2 h-6 bg-red-500 rounded"></div>
                <span>Vitals & Measurements</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Heart className="h-5 w-5 text-red-600" />
                  <span className="font-medium">Blood Pressure</span>
                </div>
                <span className="text-lg font-semibold text-red-700">{patient.blood_pressure}</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-orange-600" />
                  <span className="font-medium">Blood Sugar</span>
                </div>
                <span className="text-lg font-semibold text-orange-700">{patient.blood_sugar} mg/dL</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-blue-600" />
                  <span className="font-medium">Cholesterol</span>
                </div>
                <span className="text-lg font-semibold text-blue-700">{patient.cholesterol} mg/dL</span>
              </div>
            </CardContent>
          </Card>

          {/* Lifestyle Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <div className="w-2 h-6 bg-green-500 rounded"></div>
                <span>Lifestyle Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Smoking Status</label>
                  <Badge variant={patient.smoking_status === 'Never' ? 'secondary' : 'destructive'} className="mt-1">
                    {patient.smoking_status}
                  </Badge>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Alcohol Consumption</label>
                  <Badge variant="outline" className="mt-1">
                    {patient.alcohol_consumption}
                  </Badge>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Exercise Frequency</label>
                  <Badge variant="outline" className="mt-1">
                    {patient.exercise_frequency}
                  </Badge>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Activity Level</label>
                  <Badge variant="outline" className="mt-1">
                    {patient.activity_level}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PatientDetailView;
