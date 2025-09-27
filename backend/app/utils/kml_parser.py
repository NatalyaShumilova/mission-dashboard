import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class KMLParsingError(Exception):
    """Custom exception for KML parsing errors"""
    pass

def parse_kml_file(file_content: str) -> Dict:
    """
    Parse KML file content and extract waypoints from DJI drone mission files.
    
    Args:
        file_content (str): Raw KML file content as string
        
    Returns:
        Dict: Parsed data containing waypoints and metadata
        
    Raises:
        KMLParsingError: If KML parsing fails
    """
    try:
        # Parse XML content
        root = ET.fromstring(file_content)
        
        # Extract waypoints from placemarks
        waypoints = _extract_waypoints(root)
        
        logger.info(f"Successfully parsed KML: {len(waypoints)} waypoints found")
        
        return {
            'waypoints': waypoints,
            'waypoint_count': len(waypoints)
        }
        
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {str(e)}")
        raise KMLParsingError(f"Invalid KML file format: {str(e)}")
    except Exception as e:
        logger.error(f"KML parsing error: {str(e)}")
        raise KMLParsingError(f"Failed to parse KML file: {str(e)}")

def _extract_waypoints(root: ET.Element) -> List[Dict]:
    """Extract waypoints from KML placemarks"""
    waypoints = []
    
    # Define namespaces based on the example KML
    namespaces = {
        'kml': 'http://www.opengis.net/kml/2.2',
        'wpml': 'http://www.dji.com/wpmz/1.0.6'
    }
    
    # Find all Placemark elements
    placemarks = root.findall('.//kml:Placemark', namespaces)
    
    for placemark in placemarks:
        waypoint = _parse_placemark(placemark, namespaces)
        if waypoint:
            waypoints.append(waypoint)
    
    # Sort waypoints by index to maintain order
    waypoints.sort(key=lambda x: x.get('index', 0))
    
    return waypoints

def _parse_placemark(placemark: ET.Element, namespaces: Dict[str, str]) -> Optional[Dict]:
    """Parse a single placemark element to extract waypoint data"""
    try:
        # Find Point coordinates
        point = placemark.find('.//kml:Point', namespaces)
        if point is None:
            return None
            
        coords_elem = point.find('kml:coordinates', namespaces)
        if coords_elem is None or not coords_elem.text:
            return None
        
        # Parse coordinates (format: longitude,latitude)
        coords_text = coords_elem.text.strip()
        longitude, latitude = _parse_coordinates(coords_text)
        
        # Extract waypoint index
        index_elem = placemark.find('wpml:index', namespaces)
        index = int(index_elem.text) if index_elem is not None and index_elem.text else 0
        
        # Extract execute height (altitude)
        height_elem = placemark.find('wpml:executeHeight', namespaces)
        altitude = float(height_elem.text) if height_elem is not None and height_elem.text else None
        
        return {
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'index': index
        }
        
    except Exception as e:
        logger.warning(f"Failed to parse placemark: {str(e)}")
        return None

def _parse_coordinates(coords_text: str) -> tuple[float, float]:
    """Parse coordinate string into longitude, latitude"""
    # Clean up the coordinates text and split by comma
    coords_text = coords_text.strip()
    coord_parts = coords_text.split(',')
    
    if len(coord_parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coords_text}")
    
    try:
        longitude = float(coord_parts[0])
        latitude = float(coord_parts[1])
        
        return longitude, latitude
        
    except ValueError as e:
        raise ValueError(f"Invalid coordinate values: {coords_text}") from e
