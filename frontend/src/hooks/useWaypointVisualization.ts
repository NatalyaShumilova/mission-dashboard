import mapboxgl from 'mapbox-gl';
import { Waypoint } from '../services/missionService';

interface UseWaypointVisualizationReturn {
  updateWaypoints: (waypoints: Waypoint[]) => void;
  cleanupWaypoints: () => void;
}

export const useWaypointVisualization = (
  map: React.RefObject<mapboxgl.Map | null>,
  mapLoaded: boolean
): UseWaypointVisualizationReturn => {

  const cleanupWaypoints = () => {
    if (!map.current) return;

    if (map.current.getSource('waypoints')) {
      // Remove layers and sources
      map.current.removeLayer('waypoints-layer');
      map.current.removeLayer('waypoint-labels');
      map.current.removeSource('waypoints');
    }
    if (map.current.getSource('flight-path')) {
      map.current.removeLayer('flight-path-layer');
      map.current.removeSource('flight-path');
    }
  };

  const updateWaypoints = (waypoints: Waypoint[]) => {
    if (!map.current || !mapLoaded) return;

    // Define event handlers
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

    // Clean up existing waypoints first
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

    // Add event listeners
    map.current.on('click', 'waypoints-layer', handleWaypointClick);
    map.current.on('mouseenter', 'waypoints-layer', handleWaypointMouseEnter);
    map.current.on('mouseleave', 'waypoints-layer', handleWaypointMouseLeave);
  };

  return {
    updateWaypoints,
    cleanupWaypoints
  };
};
