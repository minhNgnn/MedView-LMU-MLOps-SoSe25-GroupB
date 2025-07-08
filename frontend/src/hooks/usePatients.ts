import { useEffect, useState } from 'react';

export interface Patient {
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

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/patients')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch patients');
        return res.json();
      })
      .then(data => {
        setPatients(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { patients, loading, error };
} 