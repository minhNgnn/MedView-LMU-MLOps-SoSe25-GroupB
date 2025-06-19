
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { PatientData } from "@/types/health";
import { User } from "lucide-react";

interface PatientFormProps {
  onSubmit: (data: PatientData) => void;
  isLoading: boolean;
}

const PatientForm = ({ onSubmit, isLoading }: PatientFormProps) => {
  const [formData, setFormData] = useState<PatientData>({
    age: 45,
    gender: 'male',
    bloodPressure: 120,
    bloodSugar: 100,
    cholesterol: 200,
    smoker: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const updateField = (field: keyof PatientData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className="w-full">
      <CardHeader className="space-y-1">
        <CardTitle className="text-xl font-semibold flex items-center gap-2">
          <User className="h-5 w-5 text-blue-600" />
          Patient Information
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Enter patient data for health risk assessment
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="age">Age (years)</Label>
              <Input
                id="age"
                type="number"
                min="1"
                max="120"
                value={formData.age}
                onChange={(e) => updateField('age', parseInt(e.target.value) || 0)}
                className="w-full"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="gender">Gender</Label>
              <Select value={formData.gender} onValueChange={(value) => updateField('gender', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="bloodPressure">Blood Pressure (mmHg)</Label>
              <Input
                id="bloodPressure"
                type="number"
                min="60"
                max="250"
                value={formData.bloodPressure}
                onChange={(e) => updateField('bloodPressure', parseInt(e.target.value) || 0)}
                placeholder="e.g., 120"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="bloodSugar">Blood Sugar Level (mg/dL)</Label>
              <Input
                id="bloodSugar"
                type="number"
                min="50"
                max="400"
                value={formData.bloodSugar}
                onChange={(e) => updateField('bloodSugar', parseInt(e.target.value) || 0)}
                placeholder="e.g., 100"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="cholesterol">Cholesterol Level (mg/dL)</Label>
            <Input
              id="cholesterol"
              type="number"
              min="100"
              max="400"
              value={formData.cholesterol}
              onChange={(e) => updateField('cholesterol', parseInt(e.target.value) || 0)}
              placeholder="e.g., 200"
              className="w-full"
            />
          </div>

          <div className="flex items-center justify-between py-2">
            <div className="space-y-0.5">
              <Label htmlFor="smoker">Smoker</Label>
              <p className="text-sm text-muted-foreground">Does the patient smoke tobacco?</p>
            </div>
            <Switch
              id="smoker"
              checked={formData.smoker}
              onCheckedChange={(checked) => updateField('smoker', checked)}
            />
          </div>

          <Button 
            type="submit" 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
            disabled={isLoading}
          >
            {isLoading ? "Analyzing..." : "Predict Risk"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default PatientForm;
