import React, { useState } from 'react';
import PatientListView from '../components/medical/PatientListView';
import PatientDetailView from '../components/medical/PatientDetailView';
import { Patient } from '../types/medical';

const MedicalDashboard = () => {
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [view, setView] = useState<'list' | 'detail'>('list');

  const handlePatientSelect = (patient: Patient) => {
    setSelectedPatient(patient);
    setView('detail');
  };

  const handleBackToList = () => {
    setSelectedPatient(null);
    setView('list');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {view === 'list' ? (
        <PatientListView onPatientSelect={handlePatientSelect} />
      ) : (
        selectedPatient && (
          <PatientDetailView 
            patient={selectedPatient} 
            onBack={handleBackToList} 
          />
        )
      )}
    </div>
  );
};

export default MedicalDashboard;
