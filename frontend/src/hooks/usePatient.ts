import { useEffect, useState } from 'react';
import { Patient } from './usePatients';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export function usePatient(id: string | undefined) {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch(`${API_BASE_URL}/patients/${id}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch patient');
        return res.json();
      })
      .then(data => {
        setPatient(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  return { patient, loading, error };
}
