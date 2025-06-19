
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { PredictionResult } from "@/types/health";
import { Circle } from "lucide-react";

interface PredictionResultsProps {
  result: PredictionResult | null;
  isLoading: boolean;
}

const PredictionResults = ({ result, isLoading }: PredictionResultsProps) => {
  const getRiskLevel = (percentage: number) => {
    if (percentage < 30) return { level: 'Low', color: 'bg-green-500', textColor: 'text-green-700' };
    if (percentage < 70) return { level: 'Medium', color: 'bg-yellow-500', textColor: 'text-yellow-700' };
    return { level: 'High', color: 'bg-red-500', textColor: 'text-red-700' };
  };

  if (isLoading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-lg">Analyzing...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-2 bg-gray-200 rounded w-full mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
              <div className="h-2 bg-gray-200 rounded w-full"></div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-lg">Risk Assessment</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            Enter patient data and click "Predict Risk" to see results
          </p>
        </CardContent>
      </Card>
    );
  }

  const heartRisk = getRiskLevel(result.heartDiseaseRisk);
  const diabetesRisk = getRiskLevel(result.diabetesRisk);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg">Risk Assessment Results</CardTitle>
        <Badge variant="outline" className="w-fit">
          {result.confidence}% Confidence
        </Badge>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Heart Disease Risk */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Heart Disease Risk</span>
            <Badge className={`${heartRisk.color} text-white`}>
              {heartRisk.level}
            </Badge>
          </div>
          <Progress value={result.heartDiseaseRisk} className="w-full" />
          <p className="text-xs text-muted-foreground">
            {result.heartDiseaseRisk}% chance of elevated heart disease risk
          </p>
        </div>

        {/* Diabetes Risk */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Diabetes Risk</span>
            <Badge className={`${diabetesRisk.color} text-white`}>
              {diabetesRisk.level}
            </Badge>
          </div>
          <Progress value={result.diabetesRisk} className="w-full" />
          <p className="text-xs text-muted-foreground">
            {result.diabetesRisk}% chance of developing diabetes
          </p>
        </div>

        {/* Recommendations */}
        <div className="space-y-3">
          <h4 className="text-sm font-medium">Recommendations</h4>
          <div className="space-y-2">
            {result.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start gap-2">
                <Circle className="h-2 w-2 mt-2 text-blue-600 fill-current" />
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {recommendation}
                </p>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictionResults;
