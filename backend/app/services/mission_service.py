from typing import Dict, List
from app.database import db
from app.models.mission import Mission, Annotation, NoFlyZone
from app.utils.kml_parser import parse_kml_file, KMLParsingError
from app.errors import ValidationError, NotFoundError
import logging

logger = logging.getLogger(__name__)

class MissionService:
    """Service class for mission-related business logic"""
    
    @staticmethod
    def get_all_missions() -> List[Dict]:
        """Get all missions"""
        missions = Mission.query.all()
        return [mission.to_dict() for mission in missions]
    
    @staticmethod
    def get_mission_by_id(mission_id: int) -> Dict:
        """Get a mission by ID"""
        mission = Mission.query.get(mission_id)
        if not mission:
            raise NotFoundError(f"Mission with ID {mission_id} not found")
        return mission.to_dict()
    
    @staticmethod
    def create_mission_from_kml(mission_name: str, kml_content: str) -> Dict:
        """
        Create a new mission from KML file content
        
        Args:
            mission_name (str): Name for the mission
            kml_content (str): Raw KML file content
            
        Returns:
            Dict: Mission data with parsed waypoints
            
        Raises:
            ValidationError: If validation fails
            KMLParsingError: If KML parsing fails
        """
        try:
            # Validate inputs
            if not mission_name or not mission_name.strip():
                raise ValidationError("Mission name is required")
            
            if not kml_content or not kml_content.strip():
                raise ValidationError("KML content is required")
            
            # Parse KML file
            logger.info(f"Parsing KML for mission: {mission_name}")
            parsed_data = parse_kml_file(kml_content)
            
            # Create new mission
            # TODO: Save parsed waypoints to avoid re-parsing later
            new_mission = Mission(
                name=mission_name.strip(),
                kml_data=kml_content
            )
            
            db.session.add(new_mission)
            db.session.commit()
            
            logger.info(f"Created mission {new_mission.id} with {parsed_data['waypoint_count']} waypoints")
            
            # Return structured response
            return {
                'mission': {
                    'id': new_mission.id,
                    'name': new_mission.name
                },
                'waypoints': parsed_data['waypoints'],
                'waypoint_count': parsed_data['waypoint_count']
            }
            
        except KMLParsingError as e:
            logger.error(f"KML parsing failed for mission {mission_name}: {str(e)}")
            raise ValidationError(f"KML parsing failed: {str(e)}")
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to create mission {mission_name}: {str(e)}")
            db.session.rollback()
            raise ValidationError(f"Failed to create mission: {str(e)}")
    
    @staticmethod
    def update_mission(mission_id: int, name: str = None, kml_data: str = None) -> Dict:
        """Update an existing mission"""
        mission = Mission.query.get(mission_id)
        if not mission:
            raise NotFoundError(f"Mission with ID {mission_id} not found")
        
        if name is not None:
            mission.name = name
        if kml_data is not None:
            mission.kml_data = kml_data
            
        db.session.commit()
        return mission.to_dict()
    
    @staticmethod
    def delete_mission(mission_id: int) -> None:
        """Delete a mission"""
        mission = Mission.query.get(mission_id)
        if not mission:
            raise NotFoundError(f"Mission with ID {mission_id} not found")
        
        db.session.delete(mission)
        db.session.commit()
    
    @staticmethod
    def create_annotation(mission_id: int, latitude: float, longitude: float, note: str = None) -> Dict:
        """Create an annotation for a mission"""
        mission = Mission.query.get(mission_id)
        if not mission:
            raise NotFoundError(f"Mission with ID {mission_id} not found")
        
        new_annotation = Annotation(
            mission_id=mission_id,
            latitude=latitude,
            longitude=longitude,
            note=note
        )
        
        db.session.add(new_annotation)
        db.session.commit()
        return new_annotation.to_dict()
    
    @staticmethod
    def create_no_fly_zone(mission_id: int, coordinates: str, note: str = None) -> Dict:
        """Create a no-fly zone for a mission"""
        mission = Mission.query.get(mission_id)
        if not mission:
            raise NotFoundError(f"Mission with ID {mission_id} not found")
        
        new_no_fly_zone = NoFlyZone(
            mission_id=mission_id,
            coordinates=coordinates,
            note=note
        )
        
        db.session.add(new_no_fly_zone)
        db.session.commit()
        return new_no_fly_zone.to_dict()
