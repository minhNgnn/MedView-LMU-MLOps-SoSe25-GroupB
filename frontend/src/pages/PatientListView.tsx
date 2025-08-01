import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Clock, User, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { usePatients } from '@/hooks/usePatients';

const PatientListView: React.FC = () => {
  const navigate = useNavigate();
  const { patients, loading, error } = usePatients();

  if (loading) {
    return <div className="p-8 text-center">Loading patients...</div>;
  }
  if (error) {
    return <div className="p-8 text-center text-red-500">{error}</div>;
  }

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
                onClick={() => navigate(`/patients/${patient.id}`)}
                className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <Avatar className="h-12 w-12">
                  <AvatarFallback className="bg-blue-100 text-blue-600">
                    {patient.first_name[0]}{patient.last_name[0]}
                  </AvatarFallback>
                </Avatar>

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">{patient.first_name} {patient.last_name}</h3>
                    <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      {patient.id}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{patient.address}</p>
                  <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                    <Clock className="h-3 w-3" />
                    Age: {patient.age} | Gender: {patient.gender} | Phone: {patient.phone_number}
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
