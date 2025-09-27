from app.database import db

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    kml_data = db.Column(db.Text, nullable=False)
    waypoints = db.relationship('Waypoint', backref='mission', lazy=True, cascade='all, delete-orphan')
    annotations = db.relationship('Annotation', backref='mission', lazy=True)
    no_fly_zones = db.relationship('NoFlyZone', backref='mission', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'kml_data': self.kml_data,
            'waypoints': [waypoint.to_dict() for waypoint in self.waypoints],
            'waypoint_count': len(self.waypoints),
            'annotations': [annotation.to_dict() for annotation in self.annotations],
            'no_fly_zones': [no_fly_zone.to_dict() for no_fly_zone in self.no_fly_zones]
        }

class Waypoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=True)
    index = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'mission_id': self.mission_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'index': self.index
        }

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'mission_id': self.mission_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'note': self.note
        }

class NoFlyZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    coordinates = db.Column(db.Text, nullable=False)
    note = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'mission_id': self.mission_id,
            'coordinates': self.coordinates,
            'note': self.note
        }
