import os
from app import create_app
from app.database import db
from app.models.mission import Mission, Annotation, NoFlyZone

def init_db():
    app = create_app()
    with app.app_context():
        # Create database directory if it doesn't exist
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if db_path and os.path.dirname(db_path):
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
