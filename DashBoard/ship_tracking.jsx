import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Bot, AlertTriangle, Sparkles, Package, Ship, Navigation } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import ShipmentOrderDetails from './ShipmentOrderDetails';
import SalesChatbot from "./saleschatbot";
import ShipRouteMap from './ShipRouteMap'; 

const ShipTrackingDashboard = () => {
  // Existing state
  const [vessels, setVessels] = useState([
    {
      id: 1,
      name: "Cargo Vessel Alpha",
      position: { lat: 25.7741, lng: -80.1867 },
      destination: { lat: 26.1224, lng: -80.1373 },
      speed: 15,
      heading: 45,
      type: "cargo",
      eta: new Date(Date.now() + 3600000),
      history: Array.from({ length: 24 }, (_, i) => ({
        time: new Date(Date.now() - i * 3600000),
        speed: 15 + Math.random() * 5,
        position: {
          lat: 25.7741 + (i * 0.01),
          lng: -80.1867 + (i * 0.01)
        }
      }))
    },
    {
      id: 2,
      name: "Tanker Beta",
      position: { lat: 25.8741, lng: -80.2867 },
      destination: { lat: 26.2224, lng: -80.2373 },
      speed: 12,
      heading: 35,
      type: "tanker",
      eta: new Date(Date.now() + 7200000),
      history: Array.from({ length: 24 }, (_, i) => ({
        time: new Date(Date.now() - i * 3600000),
        speed: 12 + Math.random() * 5,
        position: {
          lat: 25.8741 + (i * 0.01),
          lng: -80.2867 + (i * 0.01)
        }
      }))
    }
  ]);

  const [weather, setWeather] = useState([
    {
      position: { lat: 25.7741, lng: -80.1867 },
      temperature: 28,
      windSpeed: 15,
      windDirection: 90,
      conditions: "Clear"
    },
    {
      position: { lat: 26.1224, lng: -80.1373 },
      temperature: 27,
      windSpeed: 12,
      windDirection: 85,
      conditions: "Partly Cloudy"
    }
  ]);
  const [selectedVessel, setSelectedVessel] = useState(null);
  
  // AI-related state
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Simulated AI analysis function
  const analyzeRouteRisks = (vesselData) => {
    return {
      weatherRisk: Math.random() > 0.7 ? 'high' : 'low',
      congestionRisk: Math.random() > 0.6 ? 'medium' : 'low',
      optimalRoute: 'Suggested route adjustment: 5° north to avoid incoming storm',
      estimatedFuel: Math.floor(Math.random() * 1000) + 2000 + ' liters',
      predictedDelay: Math.random() > 0.5 ? '2 hours due to port congestion' : null
    };
  };

  // AI Query Handler
  const handleAiQuery = async () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      const response = generateAiResponse(aiQuery);
      setAiResponse(response);
      setIsAnalyzing(false);
    }, 1000);
  };

  // Simulated AI response generation
  const generateAiResponse = (query) => {
    const responses = {
      weather: "Based on current weather patterns, I recommend adjusting the route 5° north to avoid the developing storm system. This should save approximately 2 hours of travel time and reduce fuel consumption by 12%.",
      congestion: "Port analysis shows peak congestion in 3 hours. Recommended arrival time adjustment: +2 hours to minimize waiting time. Alternative port suggestion: Port B has 60% less current traffic.",
      efficiency: "Route optimization analysis complete. Suggested changes: 1) Adjust speed to 14 knots to hit optimal fuel efficiency 2) Use currents at waypoint C for 5% fuel savings 3) Updated ETA: 14:30 with these optimizations.",
    };

    if (query.toLowerCase().includes('weather')) return responses.weather;
    if (query.toLowerCase().includes('congestion')) return responses.congestion;
    return responses.efficiency;
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* AI Assistant Panel */}
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5" />
              AI Assistant
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Ask about weather, routes, or port conditions..."
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  className="flex-1 p-2 border rounded"
                />
                <button
                  onClick={handleAiQuery}
                  disabled={isAnalyzing}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
                >
                  {isAnalyzing ? "Analyzing..." : "Ask AI"}
                </button>
              </div>
              {aiResponse && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-start gap-2">
                    <Sparkles className="h-5 w-5 text-blue-500 mt-1" />
                    <div className="flex-1">{aiResponse}</div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
  
        {/* Vessel List with AI Insights */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Ship className="h-5 w-5" />
              Vessels with AI Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {vessels.map((vessel) => {
                const risks = analyzeRouteRisks(vessel);
                return (
                  <div
                    key={vessel.id}
                    className={`p-4 rounded-lg cursor-pointer transition-colors ${
                      selectedVessel?.id === vessel.id
                        ? "bg-blue-100"
                        : "bg-slate-50 hover:bg-slate-100"
                    }`}
                    onClick={() => setSelectedVessel(vessel)}
                  >
                    <div className="font-medium">{vessel.name}</div>
                    <div className="text-sm text-slate-500 mt-1">
                      Speed: {vessel.speed.toFixed(1)} knots
                    </div>
                    {risks.weatherRisk === "high" && (
                      <Alert className="mt-2 bg-yellow-50">
                        <AlertTriangle className="h-4 w-4" />
                        <AlertTitle>Weather Risk Alert</AlertTitle>
                        <AlertDescription>
                          Storm system detected ahead. Route adjustment
                          recommended.
                        </AlertDescription>
                      </Alert>
                    )}
                    <div className="mt-2 text-sm">
                      <div className="text-green-600">
                        AI Optimized ETA: {vessel.eta.toLocaleTimeString()}
                      </div>
                      <div className="text-blue-600">
                        Predicted Fuel Usage: {risks.estimatedFuel}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
  
        {/* Main Map Area with AI Overlays */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Navigation className="h-5 w-5" />
              AI-Enhanced Live Tracking
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-96">
              <ShipRouteMap /> {/* Add the ShipRouteMap component here */}
            </div>
          </CardContent>
        </Card>
  
        {/* AI Predictions Panel */}
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              AI Predictions & Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-green-50 rounded-lg">
                <h3 className="font-medium">Weather Impact Analysis</h3>
                <p className="text-sm mt-2">
                  AI predicts 15% faster journey times by adjusting routes to
                  utilize favorable wind patterns over the next 12 hours.
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <h3 className="font-medium">Port Congestion Forecast</h3>
                <p className="text-sm mt-2">
                  Machine learning models predict reduced port congestion in 4
                  hours. Recommended arrival window: 14:00-16:00.
                </p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <h3 className="font-medium">Efficiency Opportunities</h3>
                <p className="text-sm mt-2">
                  AI suggests optimal speed adjustments could reduce fuel
                  consumption by 8% across the fleet.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
  
        {/* Shipment Details Component */}
        <Card className="md:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="h-5 w-5" />
              Shipment Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ShipmentOrderDetails />
            <SalesChatbot />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ShipTrackingDashboard;