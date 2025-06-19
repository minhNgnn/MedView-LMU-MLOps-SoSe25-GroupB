
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PatientRecord } from "@/types/health";
import { User } from "lucide-react";

const RecentPatients = () => {
  // Mock data for recent patients
  const recentPatients: PatientRecord[] = [
    {
      id: "1",
      name: "Maria Schmidt",
      age: 54,
      gender: "Female",
      lastVisit: "2024-06-10",
      riskLevel: "medium"
    },
    {
      id: "2", 
      name: "Hans Mueller",
      age: 67,
      gender: "Male",
      lastVisit: "2024-06-08",
      riskLevel: "high"
    },
    {
      id: "3",
      name: "Anna Weber",
      age: 34,
      gender: "Female", 
      lastVisit: "2024-06-07",
      riskLevel: "low"
    },
    {
      id: "4",
      name: "Klaus Fischer",
      age: 48,
      gender: "Male",
      lastVisit: "2024-06-05",
      riskLevel: "medium"
    }
  ];

  const getRiskBadge = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low':
        return <Badge className="bg-green-500 text-white">Low</Badge>;
      case 'medium':
        return <Badge className="bg-yellow-500 text-white">Medium</Badge>;
      case 'high':
        return <Badge className="bg-red-500 text-white">High</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <User className="h-4 w-4 text-blue-600" />
          Recent Patients
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {recentPatients.map((patient) => (
            <div 
              key={patient.id}
              className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-medium text-sm">{patient.name}</h4>
                  <p className="text-xs text-muted-foreground">
                    {patient.age} years, {patient.gender}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Last visit: {formatDate(patient.lastVisit)}
                  </p>
                </div>
                <div className="ml-2">
                  {getRiskBadge(patient.riskLevel)}
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-4 pt-3 border-t border-gray-200">
          <button className="text-xs text-blue-600 hover:text-blue-800 transition-colors">
            View all patients →
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default RecentPatients;
