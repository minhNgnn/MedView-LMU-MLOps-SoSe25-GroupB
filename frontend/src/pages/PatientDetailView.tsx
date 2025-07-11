import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { ArrowLeft, Home, Phone, Mail, MapPin, Heart, Activity, Zap, AlertTriangle, CheckCircle } from 'lucide-react';
import { Patient } from '@/types/medical';
import { usePatient } from '@/hooks/usePatient';
import ImageUploadAndPredict from './ImageUploadAndPredict';

const PatientDetailView = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { patient, loading, error } = usePatient(id);

  if (loading) {
    return <div className="p-8 text-center">Loading patient details...</div>;
  }
  if (error) {
    return <div className="p-8 text-center text-red-500">{error}</div>;
  }
  if (!patient) {
    return <div className="p-8 text-center text-red-500">Patient not found.</div>;
  }

  const handleGoHome = () => {
    navigate('/');
  };

  const handleBack = () => {
    navigate('/patients');
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
                onClick={handleBack}
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

          {/* Image Upload and Predict Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <div className="w-2 h-6 bg-purple-500 rounded"></div>
                <span>Image Prediction</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <ImageUploadAndPredict />
            </CardContent>
          </Card>

          {/* Brain Scan & ML Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <div className="w-2 h-6 bg-purple-500 rounded"></div>
                <span>Brain Scan & ML Analysis</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                <img
                  src={patient.brainScan?.imageUrl}
                  alt="Brain Scan"
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Tumor Detection</span>
                  <div className="flex items-center space-x-2">
                    {patient.brainScan?.hasTumor ? (
                      <AlertTriangle className="h-5 w-5 text-red-500" />
                    ) : (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    )}
                    <Badge variant={patient.brainScan?.hasTumor ? 'destructive' : 'secondary'}>
                      {patient.brainScan?.hasTumor ? 'Tumor Detected' : 'No Tumor'}
                    </Badge>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-500">Diagnosis</label>
                  <p className="text-sm text-gray-900 mt-1">{patient.brainScan?.diagnosis}</p>
                </div>

                {patient.brainScan?.mlAnalysis && (
                  <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-700 mb-2">ML Analysis</h4>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">Cancer Probability</span>
                        <span className="font-semibold text-gray-700">
                          {patient.brainScan.mlAnalysis.cancerProbability}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-400 h-2 rounded-full"
                          style={{ width: `${patient.brainScan.mlAnalysis.cancerProbability}%` }}
                        ></div>
                      </div>
                      <p className="text-sm text-gray-700 mt-2">
                        {patient.brainScan.mlAnalysis.reasoning}
                      </p>
                    </div>
                  </div>
                )}

                <div>
                  <label className="text-sm font-medium text-gray-500">Scan Date</label>
                  <p className="text-sm text-gray-900">{patient.brainScan?.scanDate}</p>
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
