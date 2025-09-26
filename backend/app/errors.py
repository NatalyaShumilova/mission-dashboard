"""Error handlers and custom exceptions for the application."""

from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API errors."""
    status_code = 500
    message = "Internal server error"
    
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        result = {'error': self.message}
        if self.payload:
            result.update(self.payload)
        return result

class ValidationError(APIError):
    """Raised when request validation fails."""
    status_code = 400
    message = "Validation error"

class NotFoundError(APIError):
    """Raised when a resource is not found."""
    status_code = 404
    message = "Resource not found"

class ConflictError(APIError):
    """Raised when there's a conflict with the current state."""
    status_code = 409
    message = "Conflict with current state"

def register_error_handlers(app):
    """Register error handlers with the Flask app."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        logger.error(f"API Error: {error.message}", exc_info=True)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle bad request errors."""
        logger.warning(f"Bad request: {error}")
        return jsonify({
            'error': 'Bad request',
            'message': 'The request could not be understood by the server'
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle not found errors."""
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle method not allowed errors."""
        return jsonify({
            'error': 'Method not allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle internal server errors."""
        logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle any unexpected errors."""
        logger.error(f"Unexpected error: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
