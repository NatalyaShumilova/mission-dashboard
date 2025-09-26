"""Utility functions and response helpers for the API."""

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

def paginate_query(query, page=1, per_page=20, max_per_page=100):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-based)
        per_page: Items per page
        max_per_page: Maximum items per page allowed
    
    Returns:
        dict with pagination info and items
    """
    # Ensure per_page doesn't exceed maximum
    per_page = min(per_page, max_per_page)
    
    # Get paginated results
    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in paginated.items],
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'next_page': paginated.next_num if paginated.has_next else None,
            'prev_page': paginated.prev_num if paginated.has_prev else None
        }
    }

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
