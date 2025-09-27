# Utils package for utility functions

from flask import request
from datetime import datetime
import uuid

def generate_request_id():
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())[:8]

def add_request_middleware(app):
    """Add request middleware for ID generation and timing."""
    
    @app.before_request
    def before_request():
        request.request_id = generate_request_id()
        request.start_time = datetime.utcnow()
    
    @app.after_request
    def after_request(response):
        # Add request ID to response headers
        response.headers['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        
        # Add processing time
        if hasattr(request, 'start_time'):
            processing_time = (datetime.utcnow() - request.start_time).total_seconds()
            response.headers['X-Processing-Time'] = f"{processing_time:.3f}s"
        
        return response
