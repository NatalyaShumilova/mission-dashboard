from flask import Blueprint, request, jsonify
from app.database import db
from app.models.mission import Mission, Annotation, NoFlyZone

bp = Blueprint('missions', __name__, url_prefix='/api/missions')

@bp.route('/', methods=['GET'])
def get_missions():
    missions = Mission.query.all()
    return jsonify([mission.to_dict() for mission in missions])

@bp.route('/<int:id>', methods=['GET'])
def get_mission(id):
    mission = Mission.query.get_or_404(id)
    return jsonify(mission.to_dict())

@bp.route('/', methods=['POST'])
def create_mission():
    data = request.get_json()
    new_mission = Mission(
        name=data['name'],
        kml_data=data['kml_data']
    )
    db.session.add(new_mission)
    db.session.commit()
    return jsonify(new_mission.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_mission(id):
    mission = Mission.query.get_or_404(id)
    data = request.get_json()
    mission.name = data.get('name', mission.name)
    mission.kml_data = data.get('kml_data', mission.kml_data)
    db.session.commit()
    return jsonify(mission.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_mission(id):
    mission = Mission.query.get_or_404(id)
    db.session.delete(mission)
    db.session.commit()
    return '', 204

@bp.route('/<int:mission_id>/annotations', methods=['POST'])
def create_annotation(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    data = request.get_json()
    new_annotation = Annotation(
        mission_id=mission.id,
        latitude=data['latitude'],
        longitude=data['longitude'],
        note=data.get('note')
    )
    db.session.add(new_annotation)
    db.session.commit()
    return jsonify(new_annotation.to_dict()), 201

@bp.route('/<int:mission_id>/no_fly_zones', methods=['POST'])
def create_no_fly_zone(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    data = request.get_json()
    new_no_fly_zone = NoFlyZone(
        mission_id=mission.id,
        coordinates=data['coordinates'],
        note=data.get('note')
    )
    db.session.add(new_no_fly_zone)
    db.session.commit()
    return jsonify(new_no_fly_zone.to_dict()), 201
