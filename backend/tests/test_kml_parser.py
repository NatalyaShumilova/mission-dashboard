import unittest
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.utils.kml_parser import parse_kml_file, KMLParsingError


class TestKMLParser(unittest.TestCase):
    """Unit tests for KML parser functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.example_kml_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'memory-bank', 'example.kml'
        )
    
    def test_parse_example_kml_file(self):
        """Test parsing the example KML file"""
        # Read the example KML file
        with open(self.example_kml_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()
        
        # Parse the KML
        result = parse_kml_file(kml_content)
        
        # Verify structure
        self.assertIn('waypoints', result)
        self.assertIn('waypoint_count', result)
        self.assertIsInstance(result['waypoints'], list)
        self.assertIsInstance(result['waypoint_count'], int)
        
        # Verify waypoint count matches list length
        self.assertEqual(result['waypoint_count'], len(result['waypoints']))
        
        # Verify we have waypoints (example KML should have 28 waypoints)
        self.assertGreater(result['waypoint_count'], 0)
        self.assertEqual(result['waypoint_count'], 28)
    
    def test_waypoint_structure(self):
        """Test that waypoints have correct structure"""
        with open(self.example_kml_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()
        
        result = parse_kml_file(kml_content)
        waypoints = result['waypoints']
        
        # Test first waypoint structure
        first_waypoint = waypoints[0]
        self.assertIn('latitude', first_waypoint)
        self.assertIn('longitude', first_waypoint)
        self.assertIn('altitude', first_waypoint)
        self.assertIn('index', first_waypoint)
        
        # Verify data types
        self.assertIsInstance(first_waypoint['latitude'], float)
        self.assertIsInstance(first_waypoint['longitude'], float)
        self.assertIsInstance(first_waypoint['index'], int)
        # altitude can be float or None
        self.assertTrue(
            isinstance(first_waypoint['altitude'], (float, type(None)))
        )
    
    def test_waypoints_sorted_by_index(self):
        """Test that waypoints are sorted by index"""
        with open(self.example_kml_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()
        
        result = parse_kml_file(kml_content)
        waypoints = result['waypoints']
        
        # Extract indices
        indices = [wp['index'] for wp in waypoints]
        
        # Verify they are sorted
        self.assertEqual(indices, sorted(indices))
        
        # Verify they start from 0 and are consecutive
        expected_indices = list(range(len(waypoints)))
        self.assertEqual(indices, expected_indices)
    
    def test_coordinate_ranges(self):
        """Test that coordinates are in expected ranges for Auckland area"""
        with open(self.example_kml_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()
        
        result = parse_kml_file(kml_content)
        waypoints = result['waypoints']
        
        latitudes = [wp['latitude'] for wp in waypoints]
        longitudes = [wp['longitude'] for wp in waypoints]
        
        # Auckland area coordinates
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lng, max_lng = min(longitudes), max(longitudes)
        
        # Verify reasonable ranges for Auckland
        self.assertTrue(-37.5 < min_lat < -36.5, f"Latitude range seems wrong: {min_lat}")
        self.assertTrue(-37.5 < max_lat < -36.5, f"Latitude range seems wrong: {max_lat}")
        self.assertTrue(174.5 < min_lng < 175.0, f"Longitude range seems wrong: {min_lng}")
        self.assertTrue(174.5 < max_lng < 175.0, f"Longitude range seems wrong: {max_lng}")
    
    def test_empty_kml_raises_error(self):
        """Test that empty KML raises KMLParsingError"""
        with self.assertRaises(KMLParsingError):
            parse_kml_file("")
    
    def test_malformed_xml_raises_error(self):
        """Test that malformed XML raises KMLParsingError"""
        malformed_xml = "<kml><Document><unclosed_tag></Document></kml>"
        
        with self.assertRaises(KMLParsingError):
            parse_kml_file(malformed_xml)
    
    def test_kml_without_waypoints(self):
        """Test KML without waypoints returns empty list"""
        kml_without_waypoints = '''<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
          <Document>
            <name>Empty Mission</name>
          </Document>
        </kml>'''
        
        result = parse_kml_file(kml_without_waypoints)
        
        self.assertEqual(result['waypoint_count'], 0)
        self.assertEqual(len(result['waypoints']), 0)


if __name__ == '__main__':
    # Create tests directory if it doesn't exist
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    # Run the tests
    unittest.main(verbosity=2)
