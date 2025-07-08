import React from 'react';
import PatientListView from '@/components/medical/PatientListView';

const MedicalDashboard = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <PatientListView onPatientSelect={() => {}} />
    </div>
  );
};

export default MedicalDashboard;
