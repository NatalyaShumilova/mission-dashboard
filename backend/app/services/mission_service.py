from typing import Dict, List
from app.database import db
from app.models.mission import Mission, Waypoint, Annotation, NoFlyZone
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
        """
        try:
            # Validate inputs
            MissionService._validate_mission_inputs(mission_name, kml_content)
            
            # Parse KML file
            logger.info(f"Parsing KML for mission: {mission_name}")
            parsed_data = parse_kml_file(kml_content)
            
            # Create mission and waypoints in database
            mission, waypoints = MissionService._create_mission_with_waypoints(
                mission_name.strip(), kml_content, parsed_data
            )
            
            logger.info(f"Created mission {mission.id} with {len(waypoints)} waypoints saved to database")
            
            # Return structured response
            return MissionService._build_mission_response(mission, waypoints)
            
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
    def _validate_mission_inputs(mission_name: str, kml_content: str) -> None:
        """Validate mission creation inputs"""
        if not mission_name or not mission_name.strip():
            raise ValidationError("Mission name is required")
        
        if not kml_content or not kml_content.strip():
            raise ValidationError("KML content is required")
    
    @staticmethod
    def _create_mission_with_waypoints(mission_name: str, kml_content: str, parsed_data: Dict) -> tuple[Mission, List[Waypoint]]:
        """Create mission and associated waypoints in database"""
        # Create new mission
        new_mission = Mission(
            name=mission_name,
            kml_data=kml_content
        )
        
        db.session.add(new_mission)
        db.session.flush()  # Flush to get the mission ID
        
        # Create waypoints
        waypoints = []
        for waypoint_data in parsed_data['waypoints']:
            waypoint = Waypoint(
                mission_id=new_mission.id,
                latitude=waypoint_data['latitude'],
                longitude=waypoint_data['longitude'],
                altitude=waypoint_data['altitude'],
                index=waypoint_data['index']
            )
            waypoints.append(waypoint)
            db.session.add(waypoint)
        
        db.session.commit()
        return new_mission, waypoints
    
    @staticmethod
    def _build_mission_response(mission: Mission, waypoints: List[Waypoint]) -> Dict:
        """Build standardized mission creation response"""
        return {
            'mission': {
                'id': mission.id,
                'name': mission.name
            },
            'waypoints': [waypoint.to_dict() for waypoint in waypoints],
            'waypoint_count': len(waypoints)
        }
    
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
