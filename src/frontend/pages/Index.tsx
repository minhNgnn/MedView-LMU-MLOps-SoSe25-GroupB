
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { Stethoscope, Users, Brain } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex items-center justify-center p-6">
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900">
            Medical Dashboard
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            A professional, clean interface designed for healthcare professionals to manage patient data and medical records efficiently.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Users className="h-12 w-12 text-blue-600 mx-auto" />
              <CardTitle>Patient Management</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Easily view and manage your patient list with quick access to essential information.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Stethoscope className="h-12 w-12 text-green-600 mx-auto" />
              <CardTitle>Medical Records</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Comprehensive patient profiles including vitals, lifestyle data, and medical history.
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Brain className="h-12 w-12 text-purple-600 mx-auto" />
              <CardTitle>AI Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Advanced brain scan analysis with ML-powered tumor detection and diagnosis support.
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        <div className="pt-8">
          <Link to="/medical">
            <Button size="lg" className="text-lg px-8 py-3">
              Access Medical Dashboard
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Index;
