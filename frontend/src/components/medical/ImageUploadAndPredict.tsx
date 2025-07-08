import React, { useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { usePredictImage } from '@/hooks/usePredictImage';

const ImageUploadAndPredict: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { predict, loading, predictedImageUrl } = usePredictImage();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      // Clear the previous prediction result when a new image is uploaded
      if (predictedImageUrl) {
        // @ts-ignore
        predict.clearResult && predict.clearResult(); // if your hook supports clearing
      }
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handlePredict = async () => {
    if (!selectedImage) return;
    try {
      await predict(selectedImage);
      // Clear uploaded image and preview after prediction
      setSelectedImage(null);
      setPreviewUrl(null);
    } catch {
      alert('Prediction failed.');
    }
  };

  return (
    <div className="flex flex-col items-start space-y-4">
      <div className="flex items-center space-x-4">
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleImageChange}
        />
        <Button variant="outline" onClick={handleUploadClick}>
          Upload Image
        </Button>
        {selectedImage && (
          <Button onClick={handlePredict} disabled={loading}>
            {loading ? 'Predicting...' : 'Predict'}
          </Button>
        )}
      </div>
      {/* Show preview if available, otherwise show prediction result */}
      {previewUrl ? (
        <div className="w-full flex justify-center">
          <img
            src={previewUrl}
            alt="Selected"
            className="mt-2 rounded border w-full h-auto"
          />
        </div>
      ) : predictedImageUrl && (
        <div className="mt-4 w-full">
          <div className="font-semibold mb-2">Prediction Result:</div>
          <img
            src={predictedImageUrl}
            alt="Prediction Result"
            className="rounded border w-full h-auto"
          />
        </div>
      )}
    </div>
  );
};

export default ImageUploadAndPredict;
