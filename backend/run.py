import os
from app import create_app

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    # Run the application
    app.run(
        host=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_RUN_PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
