# API response helpers and utilities
from flask import jsonify, request
from datetime import datetime
import uuid

def generate_request_id():
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())[:8]

def api_response(data=None, message=None, status_code=200, meta=None):
    """
    Create a standardized API response.
    
    Args:
        data: The response data (dict, list, or None)
        message: Optional message string
        status_code: HTTP status code (default: 200)
        meta: Optional metadata dict
    
    Returns:
        Flask response object
    """
    response_data = {
        'success': 200 <= status_code < 400,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'request_id': getattr(request, 'request_id', generate_request_id())
    }
    
    if data is not None:
        response_data['data'] = data
    
    if message:
        response_data['message'] = message
    
    if meta:
        response_data['meta'] = meta
    
    response = jsonify(response_data)
    response.status_code = status_code
    return response

def api_error_response(message, status_code=400, details=None):
    """
    Create a standardized API error response.
    
    Args:
        message: Error message string
        status_code: HTTP status code (default: 400)
        details: Optional error details dict
    
    Returns:
        Flask response object
    """
    error_data = {
        'success': False,
        'error': {
            'message': message,
            'code': status_code
        },
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'request_id': getattr(request, 'request_id', generate_request_id())
    }
    
    if details:
        error_data['error']['details'] = details
    
    response = jsonify(error_data)
    response.status_code = status_code
    return response


def validate_json_request(required_fields=None, optional_fields=None):
    """
    Validate JSON request data.
    
    Args:
        required_fields: List of required field names
        optional_fields: List of optional field names
    
    Returns:
        dict: Validated request data
    
    Raises:
        ValueError: If validation fails
    """
    if not request.is_json:
        raise ValueError("Request must be JSON")
    
    data = request.get_json()
    if not data:
        raise ValueError("Request body cannot be empty")
    
    required_fields = required_fields or []
    optional_fields = optional_fields or []
    allowed_fields = set(required_fields + optional_fields)
    
    # Check for required fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Check for unexpected fields
    unexpected_fields = [field for field in data.keys() if field not in allowed_fields]
    if unexpected_fields:
        raise ValueError(f"Unexpected fields: {', '.join(unexpected_fields)}")
    
    # Return only allowed fields
    return {field: data[field] for field in data.keys() if field in allowed_fields}
