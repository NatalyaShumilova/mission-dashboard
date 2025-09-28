from flask import Blueprint, request
from app.services.mission_service import MissionService
from app.errors import ValidationError
from app.utils.api_helpers import api_response

bp = Blueprint('missions', __name__, url_prefix='/api/missions')

@bp.route('/', methods=['GET'])
def get_missions():
    missions = MissionService.get_all_missions()
    return api_response(data=missions)

@bp.route('/<int:id>', methods=['GET'])
def get_mission(id):
    mission = MissionService.get_mission_by_id(id)
    return api_response(data=mission)

@bp.route('/', methods=['POST'])
def create_mission():
    try:
        # Check if request contains file upload
        if 'file' not in request.files:
            raise ValidationError("No KML file provided")
        
        file = request.files['file']
        if file.filename == '':
            raise ValidationError("No file selected")
        
        # Validate file extension
        if not file.filename.lower().endswith('.kml'):
            raise ValidationError("File must be a KML file")
        
        # Get mission name from form data
        mission_name = request.form.get('name')
        if not mission_name:
            raise ValidationError("Mission name is required")
        
        # Read KML file content
        kml_content = file.read().decode('utf-8')
        
        # Create mission using service
        result = MissionService.create_mission_from_kml(mission_name, kml_content)
        
        return api_response(data=result, status_code=201)
        
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Failed to process request: {str(e)}")

@bp.route('/<int:id>', methods=['PUT'])
def update_mission(id):
    data = request.get_json()
    mission = MissionService.update_mission(
        id, 
        name=data.get('name'), 
        kml_data=data.get('kml_data')
    )
    return api_response(data=mission)

@bp.route('/<int:id>', methods=['DELETE'])
def delete_mission(id):
    MissionService.delete_mission(id)
    return api_response(message='Mission deleted successfully')

@bp.route('/<int:mission_id>/annotations', methods=['POST'])
def create_annotation(mission_id):
    data = request.get_json()
    annotation = MissionService.create_annotation(
        mission_id=mission_id,
        latitude=data['latitude'],
        longitude=data['longitude'],
        note=data.get('note')
    )
    return api_response(data=annotation, status_code=201)

@bp.route('/<int:mission_id>/no_fly_zones', methods=['POST'])
def create_no_fly_zone(mission_id):
    data = request.get_json()
    no_fly_zone = MissionService.create_no_fly_zone(
        mission_id=mission_id,
        coordinates=data['coordinates'],
        note=data.get('note')
    )
    return api_response(data=no_fly_zone, status_code=201)
