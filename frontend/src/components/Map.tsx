import React, { useEffect } from 'react';
import 'mapbox-gl/dist/mapbox-gl.css';
import './Map.scss';
import { useMapbox } from '../hooks/useMapbox';
import { useWaypointVisualization } from '../hooks/useWaypointVisualization';
import { Waypoint } from '../services/missionService';
import ErrorMessage from './ErrorMessage';
import LoadingSpinner from './LoadingSpinner';

interface MapProps {
  className?: string;
  waypoints?: Waypoint[];
}

const Map: React.FC<MapProps> = ({ className = '', waypoints = [] }) => {
  // Use custom hooks
  const { mapContainer, map, mapLoaded, error } = useMapbox();
  const { updateWaypoints, cleanupWaypoints } = useWaypointVisualization(map, mapLoaded);

  // Handle waypoint updates
  useEffect(() => {
    updateWaypoints(waypoints);
    
    // Cleanup on unmount
    return () => {
      cleanupWaypoints();
    };
  }, [waypoints, updateWaypoints, cleanupWaypoints]);

  return (
    error ? (
      <div className={`map-container ${className}`}>
        <ErrorMessage 
          title="Map Loading Error" 
          message={`${error} To use the map: 1) Sign up at mapbox.com, 2) Get your access token, 3) Set REACT_APP_MAPBOX_TOKEN environment variable, 4) Restart the server.`}
        />
      </div>
    ) : (
      <div className={`map-container ${className}`}>
        <div ref={mapContainer} className="map" />
        {!mapLoaded && <LoadingSpinner message="Loading map..." />}
      </div>
    )
  );
};

export default Map;
