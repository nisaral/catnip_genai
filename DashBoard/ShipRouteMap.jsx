import React, { useState, useEffect } from 'react';
import { Clock } from 'lucide-react';

const ShipRouteMap = () => {
  const [shipPositions, setShipPositions] = useState([
    { 
      id: 1, 
      progress: 0,
      eta: new Date(Date.now() + 3600000), // 1 hour from now
      name: "Cargo Vessel Alpha"
    },
    { 
      id: 2, 
      progress: 0,
      eta: new Date(Date.now() + 7200000), // 2 hours from now
      name: "Tanker Beta"
    }
  ]);

  // Convert lat/lng to SVG coordinates
  const mapCoords = (lat, lng) => {
    const x = ((lng - (-80.2867)) / ((-80.1373) - (-80.2867))) * 600;
    const y = ((lat - 25.7741) / (26.2224 - 25.7741)) * 400;
    return { x, y };
  };

  const routes = [
    {
      id: 1,
      start: mapCoords(25.7741, -80.1867),
      end: mapCoords(26.1224, -80.1373),
      color: "#3b82f6",
      startName: "Miami Port",
      endName: "Fort Lauderdale"
    },
    {
      id: 2,
      start: mapCoords(25.8741, -80.2867),
      end: mapCoords(26.2224, -80.2373),
      color: "#10b981",
      startName: "Port Miami",
      endName: "Port Everglades"
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setShipPositions(positions => 
        positions.map(pos => ({
          ...pos,
          // Reduced progress increment from 0.2 to 0.05 for slower movement
          progress: (pos.progress + 0.05) % 100
        }))
      );
      // Increased interval from 50ms to 200ms for slower updates
    }, 200);

    return () => clearInterval(interval);
  }, []);

  const getShipPosition = (route, progress) => {
    const x = route.start.x + ((route.end.x - route.start.x) * progress / 100);
    const y = route.start.y + ((route.end.y - route.start.y) * progress / 100);
    return { x, y };
  };

  const getTimeRemaining = (eta) => {
    const now = new Date();
    const diff = eta - now;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m`;
  };

  const getDistanceRemaining = (progress) => {
    const remaining = 100 - progress;
    return `${remaining.toFixed(1)}%`;
  };

  return (
    <div className="w-full h-full relative">
      <svg viewBox="0 0 600 400" className="w-full h-full bg-slate-100 rounded-lg">
        {/* Water texture */}
        <defs>
          <pattern id="water" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M0 10 Q5 5, 10 10 T20 10" fill="none" stroke="#e2e8f0" strokeWidth="1"/>
          </pattern>
        </defs>
        <rect width="600" height="400" fill="url(#water)"/>
        
        {/* Routes and ports */}
        {routes.map(route => (
          <g key={`route-${route.id}`}>
            {/* Route line */}
            <path
              d={`M ${route.start.x} ${route.start.y} L ${route.end.x} ${route.end.y}`}
              stroke={route.color}
              strokeWidth="2"
              strokeDasharray="5,5"
              fill="none"
            />
            
            {/* Port markers */}
            <circle cx={route.start.x} cy={route.start.y} r="5" fill="#475569"/>
            <circle cx={route.end.x} cy={route.end.y} r="5" fill="#475569"/>
            
            {/* Port labels */}
            <text x={route.start.x - 10} y={route.start.y - 10} className="text-xs fill-slate-600">{route.startName}</text>
            <text x={route.end.x - 10} y={route.end.y - 10} className="text-xs fill-slate-600">{route.endName}</text>
            
            {/* Animated ship */}
            {(() => {
              const ship = shipPositions.find(s => s.id === route.id);
              const pos = getShipPosition(route, ship.progress);
              const angle = Math.atan2(route.end.y - route.start.y, route.end.x - route.start.x) * 180 / Math.PI;
              
              return (
                <g transform={`translate(${pos.x}, ${pos.y}) rotate(${angle})`}>
                  <path
                    d="M-8,-4 L8,0 L-8,4 Z"
                    fill={route.color}
                  />
                </g>
              );
            })()}
          </g>
        ))}
      </svg>

      {/* Voyage information overlay */}
      <div className="absolute top-4 right-4 space-y-4">
        {shipPositions.map(ship => {
          const route = routes.find(r => r.id === ship.id);
          return (
            <div 
              key={ship.id} 
              className="bg-white/90 p-4 rounded-lg shadow-sm border-l-4"
              style={{ borderColor: route.color }}
            >
              <div className="font-medium text-sm">{ship.name}</div>
              <div className="text-xs text-slate-500 mt-1">
                Route: {route.startName} → {route.endName}
              </div>
              <div className="flex items-center gap-2 mt-2 text-xs text-slate-600">
                <Clock className="h-3 w-3"/>
                <span>ETA: {getTimeRemaining(ship.eta)}</span>
              </div>
              <div className="mt-1 text-xs text-slate-600">
                Distance remaining: {getDistanceRemaining(ship.progress)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ShipRouteMap;