import unittest
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.mission import Mission, Waypoint, Annotation, NoFlyZone


class TestModelSerialization(unittest.TestCase):
    """Unit tests for model to_dict methods"""
    
    def test_mission_to_dict(self):
        """Test Mission to_dict method"""
        mission = Mission()
        mission.id = 1
        mission.name = 'Test Mission'
        mission.kml_data = '<kml>test</kml>'
        mission.waypoints = []
        mission.annotations = []
        mission.no_fly_zones = []
        
        result = mission.to_dict()
        
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], 'Test Mission')
        self.assertEqual(result['kml_data'], '<kml>test</kml>')
        self.assertEqual(result['waypoints'], [])
        self.assertEqual(result['waypoint_count'], 0)
        self.assertEqual(result['annotations'], [])
        self.assertEqual(result['no_fly_zones'], [])
    
    def test_waypoint_to_dict(self):
        """Test Waypoint to_dict method"""
        waypoint = Waypoint()
        waypoint.id = 1
        waypoint.mission_id = 5
        waypoint.latitude = -36.8485
        waypoint.longitude = 174.7633
        waypoint.altitude = 50.0
        waypoint.index = 0
        
        result = waypoint.to_dict()
        
        expected = {
            'id': 1,
            'mission_id': 5,
            'latitude': -36.8485,
            'longitude': 174.7633,
            'altitude': 50.0,
            'index': 0
        }
        
        self.assertEqual(result, expected)
    
    def test_annotation_to_dict(self):
        """Test Annotation to_dict method"""
        annotation = Annotation()
        annotation.id = 1
        annotation.mission_id = 5
        annotation.latitude = -36.8485
        annotation.longitude = 174.7633
        annotation.note = 'Test annotation'
        
        result = annotation.to_dict()
        
        expected = {
            'id': 1,
            'mission_id': 5,
            'latitude': -36.8485,
            'longitude': 174.7633,
            'note': 'Test annotation'
        }
        
        self.assertEqual(result, expected)
    
    def test_no_fly_zone_to_dict(self):
        """Test NoFlyZone to_dict method"""
        no_fly_zone = NoFlyZone()
        no_fly_zone.id = 1
        no_fly_zone.mission_id = 5
        no_fly_zone.coordinates = '174.7633,-36.8485 174.7634,-36.8486'
        no_fly_zone.note = 'Restricted area'
        
        result = no_fly_zone.to_dict()
        
        expected = {
            'id': 1,
            'mission_id': 5,
            'coordinates': '174.7633,-36.8485 174.7634,-36.8486',
            'note': 'Restricted area'
        }
        
        self.assertEqual(result, expected)


class TestModelRelationships(unittest.TestCase):
    """Unit tests for model relationships"""
    
    def test_mission_relationships(self):
        """Test that Mission model has proper relationship attributes"""
        mission = Mission()
        
        # Test that relationship attributes exist
        self.assertTrue(hasattr(mission, 'waypoints'))
        self.assertTrue(hasattr(mission, 'annotations'))
        self.assertTrue(hasattr(mission, 'no_fly_zones'))
        
        # Test that we can assign related objects
        waypoint = Waypoint()
        waypoint.mission_id = 1
        annotation = Annotation()
        annotation.mission_id = 1
        no_fly_zone = NoFlyZone()
        no_fly_zone.mission_id = 1
        
        mission.waypoints = [waypoint]
        mission.annotations = [annotation]
        mission.no_fly_zones = [no_fly_zone]
        
        self.assertEqual(len(mission.waypoints), 1)
        self.assertEqual(len(mission.annotations), 1)
        self.assertEqual(len(mission.no_fly_zones), 1)
        self.assertEqual(mission.waypoints[0].mission_id, 1)
        self.assertEqual(mission.annotations[0].mission_id, 1)
        self.assertEqual(mission.no_fly_zones[0].mission_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
