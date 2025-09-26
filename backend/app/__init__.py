import os
from flask import Flask
from app.database import db
from config import config

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    
    # Set up logging
    from app.logging_config import setup_logging, log_request_info
    setup_logging(app)
    log_request_info(app)
    
    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Register middleware
    from app.middleware import register_middleware
    register_middleware(app)
    
    # Import models (needed for database creation)
    from app.models.mission import Mission, Annotation, NoFlyZone
    
    # Register blueprints
    from app.routes import missions
    app.register_blueprint(missions.bp)
    
    app.logger.info(f"Application created with config: {config_name}")
    
    return app
