"""Middleware functions for the application."""

from flask import request, g
import time

def add_security_headers(app):
    """Add security headers to all responses."""
    
    @app.after_request
    def security_headers(response):
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (basic)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self'"
        )
        
        # HSTS (only for HTTPS)
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

def configure_cors(app):
    """Configure CORS settings."""
    from flask_cors import CORS
    
    # Configure CORS with specific settings
    CORS(app, 
         origins=['http://localhost:3000', 'http://127.0.0.1:3000'],  # React dev server
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         supports_credentials=True,
         max_age=86400  # 24 hours
    )

def add_request_timing(app):
    """Add request timing middleware."""
    
    @app.before_request
    def start_timer():
        g.start_time = time.time()
    
    @app.after_request
    def log_timing(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            app.logger.debug(f"Request {request.method} {request.path} took {duration:.3f}s")
        return response

def add_health_check(app):
    """Add a simple health check endpoint."""
    
    @app.route('/health')
    def health_check():
        from app.utils import api_response
        return api_response(
            data={'status': 'healthy', 'service': 'mission-dashboard-api'},
            message='Service is running'
        )
    
    @app.route('/health/ready')
    def readiness_check():
        from app.utils import api_response, api_error_response
        from app.database import db
        
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return api_response(
                data={'status': 'ready', 'database': 'connected'},
                message='Service is ready'
            )
        except Exception as e:
            app.logger.error(f"Readiness check failed: {e}")
            return api_error_response(
                message='Service not ready',
                status_code=503,
                details={'database': 'disconnected', 'error': str(e)}
            )

def add_api_versioning(app):
    """Add API versioning support."""
    
    @app.before_request
    def handle_api_version():
        # Default to v1 if no version specified
        if request.path.startswith('/api/') and not request.path.startswith('/api/v'):
            # Add version info to request context
            g.api_version = 'v1'
        elif request.path.startswith('/api/v'):
            # Extract version from path
            path_parts = request.path.split('/')
            if len(path_parts) >= 3:
                g.api_version = path_parts[2]  # e.g., 'v1' from '/api/v1/missions'
            else:
                g.api_version = 'v1'
        
        # Add version to response headers
        @app.after_request
        def add_version_header(response):
            if hasattr(g, 'api_version'):
                response.headers['API-Version'] = g.api_version
            return response

def register_middleware(app):
    """Register all middleware with the Flask app."""
    
    # Security middleware
    add_security_headers(app)
    configure_cors(app)
    
    # Utility middleware
    add_request_timing(app)
    add_health_check(app)
    add_api_versioning(app)
    
    # Request/response middleware from utils
    from app.utils import add_request_middleware
    add_request_middleware(app)
    
    app.logger.info("Middleware registered successfully")
