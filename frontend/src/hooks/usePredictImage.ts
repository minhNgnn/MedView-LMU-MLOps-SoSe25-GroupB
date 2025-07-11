import { useState } from 'react';

export function usePredictImage() {
  const [loading, setLoading] = useState(false);
  const [predictedImageUrl, setPredictedImageUrl] = useState<string | null>(null);

  const predict = async (file: File) => {
    setLoading(true);
    setPredictedImageUrl(null);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Prediction failed');
      const blob = await response.blob();
      setPredictedImageUrl(URL.createObjectURL(blob));
    } catch {
      setPredictedImageUrl(null);
      throw new Error('Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return { predict, loading, predictedImageUrl };
}
