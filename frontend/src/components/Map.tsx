import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './Map.scss';

interface MapProps {
  className?: string;
}

const Map: React.FC<MapProps> = ({ className = '' }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get Mapbox token from environment variable
    const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;
    
    // Check if Mapbox token is available
    if (!MAPBOX_TOKEN) {
      setError('Mapbox access token is required. Please set REACT_APP_MAPBOX_TOKEN environment variable.');
      return;
    }

    // Set the Mapbox access token
    mapboxgl.accessToken = MAPBOX_TOKEN;

    // Initialize map only once
    if (map.current || !mapContainer.current) return;

    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/satellite-streets-v12', // Satellite view good for drone missions
        center: [174.7633, -36.8485], // Auckland, New Zealand as default center
        zoom: 10,
        attributionControl: true,
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');

      // Add scale control
      map.current.addControl(new mapboxgl.ScaleControl(), 'bottom-left');

      // Handle map load event
      map.current.on('load', () => {
        setMapLoaded(true);
        setError(null);
      });

      // Handle map errors
      map.current.on('error', (e) => {
        console.error('Mapbox error:', e);
        setError('Failed to load map. Please check your internet connection and Mapbox token.');
      });

    } catch (err) {
      console.error('Error initializing map:', err);
      setError('Failed to initialize map. Please check your Mapbox configuration.');
    }

    // Cleanup function
    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (map.current) {
        map.current.resize();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    error ? (
        <div className={`map-container ${className}`}>
            <div className="map-error">
            <div className="map-error__icon">🗺️</div>
            <div className="map-error__message">
                <h3>Map Loading Error</h3>
                <p>{error}</p>
                <div className="map-error__help">
                <p>To use the map component:</p>
                <ol>
                    <li>Sign up for a free Mapbox account at <a href="https://www.mapbox.com/" target="_blank" rel="noopener noreferrer">mapbox.com</a></li>
                    <li>Get your access token from your Mapbox account</li>
                    <li>Set the environment variable: <code>REACT_APP_MAPBOX_TOKEN=your_token_here</code></li>
                    <li>Restart the development server</li>
                </ol>
                </div>
            </div>
            </div>
        </div>
    ) : (
        <div className={`map-container ${className}`}>
        <div ref={mapContainer} className="map" />
        {!mapLoaded && (
            <div className="map-loading">
            <div className="map-loading__spinner"></div>
            <p>Loading map...</p>
            </div>
        )}
        </div>
    )
  );
};

export default Map;
