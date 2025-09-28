import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.mission_service import MissionService
from app.models.mission import Mission, Waypoint, Annotation, NoFlyZone
from app.errors import ValidationError, NotFoundError
from app.utils.kml_parser import KMLParsingError


class TestMissionService(unittest.TestCase):
    """Unit tests for MissionService business logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:wpml="http://www.dji.com/wpmz/1.0.6">
          <Document>
            <Placemark>
              <wpml:index>0</wpml:index>
              <wpml:executeHeight>50.0</wpml:executeHeight>
              <Point>
                <coordinates>174.7633,-36.8485</coordinates>
              </Point>
            </Placemark>
          </Document>
        </kml>'''
        
        self.sample_waypoints = [
            {
                'latitude': -36.8485,
                'longitude': 174.7633,
                'altitude': 50.0,
                'index': 0
            }
        ]
    
    @patch('app.services.mission_service.db.session')
    @patch('app.services.mission_service.parse_kml_file')
    def test_create_mission_from_kml_success(self, mock_parse_kml, mock_db_session):
        """Test successful mission creation from KML"""
        # Mock KML parsing
        mock_parse_kml.return_value = {
            'waypoints': self.sample_waypoints,
            'waypoint_count': 1
        }
        
        # Mock database operations
        mock_mission = MagicMock()
        mock_mission.id = 1
        mock_mission.name = 'Test Mission'
        mock_db_session.add.return_value = None
        mock_db_session.flush.return_value = None
        mock_db_session.commit.return_value = None
        
        # Create mission
        result = MissionService.create_mission_from_kml('Test Mission', self.sample_kml_content)
        
        # Verify result structure
        self.assertIn('mission', result)
        self.assertIn('waypoints', result)
        self.assertIn('waypoint_count', result)
        self.assertEqual(result['waypoint_count'], 1)
        
        # Verify database operations were called
        mock_db_session.add.assert_called()
        mock_db_session.flush.assert_called_once()
        mock_db_session.commit.assert_called_once()
        
        # Verify KML parsing was called
        mock_parse_kml.assert_called_once_with(self.sample_kml_content)
    
    def test_create_mission_empty_name_raises_validation_error(self):
        """Test that empty mission name raises ValidationError"""
        with self.assertRaises(ValidationError) as context:
            MissionService.create_mission_from_kml('', self.sample_kml_content)
        
        self.assertIn('Mission name is required', str(context.exception.message))
    
    def test_create_mission_whitespace_name_raises_validation_error(self):
        """Test that whitespace-only mission name raises ValidationError"""
        with self.assertRaises(ValidationError) as context:
            MissionService.create_mission_from_kml('   ', self.sample_kml_content)
        
        self.assertIn('Mission name is required', str(context.exception.message))
    
    def test_create_mission_empty_kml_raises_validation_error(self):
        """Test that empty KML content raises ValidationError"""
        with self.assertRaises(ValidationError) as context:
            MissionService.create_mission_from_kml('Test Mission', '')
        
        self.assertIn('KML content is required', str(context.exception.message))
    
    @patch('app.services.mission_service.parse_kml_file')
    def test_create_mission_kml_parsing_error_raises_validation_error(self, mock_parse_kml):
        """Test that KML parsing error is converted to ValidationError"""
        mock_parse_kml.side_effect = KMLParsingError('Invalid KML format')
        
        with self.assertRaises(ValidationError) as context:
            MissionService.create_mission_from_kml('Test Mission', self.sample_kml_content)
        
        self.assertIn('KML parsing failed', str(context.exception.message))
    
    @patch('app.services.mission_service.db.session')
    @patch('app.services.mission_service.parse_kml_file')
    def test_create_mission_database_error_rolls_back(self, mock_parse_kml, mock_db_session):
        """Test that database errors trigger rollback"""
        mock_parse_kml.return_value = {
            'waypoints': self.sample_waypoints,
            'waypoint_count': 1
        }
        
        # Mock database error
        mock_db_session.commit.side_effect = Exception('Database error')
        
        with self.assertRaises(ValidationError):
            MissionService.create_mission_from_kml('Test Mission', self.sample_kml_content)
        
        # Verify rollback was called
        mock_db_session.rollback.assert_called_once()
    
    @patch('app.services.mission_service.Mission')
    def test_get_all_missions(self, mock_mission_model):
        """Test getting all missions"""
        # Mock missions
        mock_mission1 = MagicMock()
        mock_mission1.to_dict.return_value = {'id': 1, 'name': 'Mission 1'}
        mock_mission2 = MagicMock()
        mock_mission2.to_dict.return_value = {'id': 2, 'name': 'Mission 2'}
        
        mock_mission_model.query.all.return_value = [mock_mission1, mock_mission2]
        
        result = MissionService.get_all_missions()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[1]['id'], 2)
    
    
    @patch('app.services.mission_service.db.session')
    @patch('app.services.mission_service.Mission')
    def test_create_annotation_success(self, mock_mission_model, mock_db_session):
        """Test successful annotation creation"""
        mock_mission = MagicMock()
        mock_mission_model.query.get.return_value = mock_mission
        
        result = MissionService.create_annotation(1, -36.8485, 174.7633, 'Test note')
        
        # Verify annotation was added to database
        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called_once()
    
    @patch('app.services.mission_service.Mission')
    def test_create_annotation_mission_not_found_raises_error(self, mock_mission_model):
        """Test that creating annotation for non-existent mission raises NotFoundError"""
        mock_mission_model.query.get.return_value = None
        
        with self.assertRaises(NotFoundError) as context:
            MissionService.create_annotation(999, -36.8485, 174.7633, 'Test note')
        
        self.assertIn('Mission with ID 999 not found', str(context.exception.message))
    
    @patch('app.services.mission_service.db.session')
    @patch('app.services.mission_service.Mission')
    def test_create_no_fly_zone_success(self, mock_mission_model, mock_db_session):
        """Test successful no-fly zone creation"""
        mock_mission = MagicMock()
        mock_mission_model.query.get.return_value = mock_mission
        
        coordinates = '174.7633,-36.8485 174.7634,-36.8486 174.7635,-36.8487'
        result = MissionService.create_no_fly_zone(1, coordinates, 'Test zone')
        
        # Verify no-fly zone was added to database
        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called_once()
    
    @patch('app.services.mission_service.Mission')
    def test_create_no_fly_zone_mission_not_found_raises_error(self, mock_mission_model):
        """Test that creating no-fly zone for non-existent mission raises NotFoundError"""
        mock_mission_model.query.get.return_value = None
        
        coordinates = '174.7633,-36.8485 174.7634,-36.8486'
        with self.assertRaises(NotFoundError) as context:
            MissionService.create_no_fly_zone(999, coordinates, 'Test zone')
        
        self.assertIn('Mission with ID 999 not found', str(context.exception.message))


if __name__ == '__main__':
    unittest.main(verbosity=2)
