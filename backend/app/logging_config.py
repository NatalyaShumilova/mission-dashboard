"""Logging configuration for the application."""

import logging
import logging.config
import os

def setup_logging(app):
    """Configure logging for the application."""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(app.instance_path), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Determine log level based on environment
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Configure logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': logging.INFO,
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'app.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': logging.ERROR,
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'errors.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            'app': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'werkzeug': {
                'level': logging.WARNING,
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': log_level,
            'handlers': ['console', 'file']
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Set up Flask app logger
    app.logger.setLevel(log_level)
    
    # Log application startup
    app.logger.info(f"Application started in {app.config.get('FLASK_ENV', 'unknown')} mode")
    
    return logging.getLogger('app')

def log_request_info(app):
    """Add request logging middleware."""
    
    @app.before_request
    def log_request():
        from flask import request
        app.logger.info(f"{request.method} {request.url} - {request.remote_addr}")
    
    @app.after_request
    def log_response(response):
        from flask import request
        app.logger.info(f"{request.method} {request.url} - {response.status_code}")
        return response
