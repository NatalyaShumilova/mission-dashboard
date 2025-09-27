import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './Map.scss';

interface Waypoint {
  id: number;
  mission_id: number;
  latitude: number;
  longitude: number;
  altitude: number | null;
  index: number;
}

interface MapProps {
  className?: string;
  waypoints?: Waypoint[];
}

const Map: React.FC<MapProps> = ({ className = '', waypoints = [] }) => {
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

  // Handle waypoint visualization
  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    // Define event handlers that we can reference for cleanup
    const handleWaypointClick = (e: mapboxgl.MapMouseEvent & { features?: mapboxgl.MapboxGeoJSONFeature[] }) => {
      if (e.features && e.features[0]) {
        const feature = e.features[0];
        const properties = feature.properties;
        
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`
            <div style="font-family: Arial, sans-serif;">
              <strong>Waypoint ${properties?.index}</strong><br/>
              ${properties?.altitude ? `Altitude: ${properties.altitude}m<br/>` : ''}
              Lat: ${e.lngLat.lat.toFixed(6)}<br/>
              Lng: ${e.lngLat.lng.toFixed(6)}
            </div>
          `)
          .addTo(map.current!);
      }
    };

    const handleWaypointMouseEnter = () => {
      if (map.current) {
        map.current.getCanvas().style.cursor = 'pointer';
      }
    };

    const handleWaypointMouseLeave = () => {
      if (map.current) {
        map.current.getCanvas().style.cursor = '';
      }
    };

    // Clean up existing waypoint layers, sources, and event listeners
    const cleanupWaypoints = () => {
      if (map.current && map.current.getSource('waypoints')) {
        // Remove event listeners first
        map.current.off('click', 'waypoints-layer', handleWaypointClick);
        map.current.off('mouseenter', 'waypoints-layer', handleWaypointMouseEnter);
        map.current.off('mouseleave', 'waypoints-layer', handleWaypointMouseLeave);
        
        // Then remove layers and sources
        map.current.removeLayer('waypoints-layer');
        map.current.removeLayer('waypoint-labels');
        map.current.removeSource('waypoints');
      }
      if (map.current && map.current.getSource('flight-path')) {
        map.current.removeLayer('flight-path-layer');
        map.current.removeSource('flight-path');
      }
    };

    // Always clean up first
    cleanupWaypoints();

    // If no waypoints, stop here (map is now clean)
    if (!waypoints.length) return;

    // Sort waypoints by index to ensure correct order
    const sortedWaypoints = [...waypoints].sort((a, b) => a.index - b.index);

    // Create GeoJSON data for waypoints
    const waypointFeatures = sortedWaypoints.map((waypoint) => ({
      type: 'Feature' as const,
      geometry: {
        type: 'Point' as const,
        coordinates: [waypoint.longitude, waypoint.latitude]
      },
      properties: {
        index: waypoint.index,
        altitude: waypoint.altitude,
        id: waypoint.id
      }
    }));

    // Create GeoJSON data for flight path
    const flightPathCoordinates = sortedWaypoints.map(waypoint => [waypoint.longitude, waypoint.latitude]);
    
    const flightPathFeature = {
      type: 'Feature' as const,
      geometry: {
        type: 'LineString' as const,
        coordinates: flightPathCoordinates
      },
      properties: {}
    };

    // Add flight path source and layer
    map.current.addSource('flight-path', {
      type: 'geojson',
      data: flightPathFeature
    });

    map.current.addLayer({
      id: 'flight-path-layer',
      type: 'line',
      source: 'flight-path',
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#ff6b35',
        'line-width': 3,
        'line-opacity': 0.8
      }
    });

    // Add waypoints source and layer
    map.current.addSource('waypoints', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: waypointFeatures
      }
    });

    // Add waypoint markers
    map.current.addLayer({
      id: 'waypoints-layer',
      type: 'circle',
      source: 'waypoints',
      paint: {
        'circle-radius': 8,
        'circle-color': '#ff6b35',
        'circle-stroke-color': '#ffffff',
        'circle-stroke-width': 2,
        'circle-opacity': 0.9
      }
    });

    // Add waypoint labels
    map.current.addLayer({
      id: 'waypoint-labels',
      type: 'symbol',
      source: 'waypoints',
      layout: {
        'text-field': ['get', 'index'],
        'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
        'text-size': 12,
        'text-offset': [0, -2],
        'text-anchor': 'bottom'
      },
      paint: {
        'text-color': '#ffffff',
        'text-halo-color': '#000000',
        'text-halo-width': 1
      }
    });

    // Fit map to show all waypoints
    if (sortedWaypoints.length > 0) {
      const coordinates = sortedWaypoints.map(waypoint => [waypoint.longitude, waypoint.latitude]);
      const bounds = coordinates.reduce((bounds, coord) => {
        return bounds.extend(coord as [number, number]);
      }, new mapboxgl.LngLatBounds(coordinates[0] as [number, number], coordinates[0] as [number, number]));

      map.current.fitBounds(bounds, {
        padding: 50,
        maxZoom: 16
      });
    }

    // Add event listeners with proper references for cleanup
    map.current.on('click', 'waypoints-layer', handleWaypointClick);
    map.current.on('mouseenter', 'waypoints-layer', handleWaypointMouseEnter);
    map.current.on('mouseleave', 'waypoints-layer', handleWaypointMouseLeave);

    // Return cleanup function
    return () => {
      cleanupWaypoints();
    };

  }, [waypoints, mapLoaded]);

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
