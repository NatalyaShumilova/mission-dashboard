# Mission Dashboard Backend API

A robust Flask-based REST API for the Drone Mission Planning Dashboard application.

## Architecture Overview

This backend application follows Flask best practices with a well-structured, production-ready architecture:

### Key Features
- **Application Factory Pattern**: Configurable app creation with environment-specific settings
- **Comprehensive Error Handling**: Custom exceptions and standardized error responses
- **Structured Logging**: File-based logging with rotation and different log levels
- **Security Middleware**: Security headers, CORS configuration, and request validation
- **API Response Framework**: Standardized response format with metadata and request tracking
- **Health Checks**: Built-in health and readiness endpoints for monitoring

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── database.py          # Database configuration
│   ├── errors.py            # Error handlers and custom exceptions
│   ├── logging_config.py    # Logging configuration
│   ├── middleware.py        # Security and utility middleware
│   ├── utils.py             # API response utilities and helpers
│   ├── models/
│   │   ├── __init__.py
│   │   └── mission.py       # Database models
│   └── routes/
│       ├── __init__.py
│       └── missions.py      # API endpoints
├── config.py                # Configuration classes
├── init_db.py              # Database initialization script
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .flaskenv              # Flask-specific environment variables
└── README.md              # This file
```

## Configuration

The application supports multiple environments through configuration classes:

- **Development**: Debug mode enabled, detailed logging
- **Production**: Optimized for production deployment
- **Testing**: In-memory database, testing-specific settings

Environment variables:
- `FLASK_ENV`: Set to 'development', 'production', or 'testing'
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Application secret key (set in production)

## API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check with database connectivity

### Missions API
- `GET /api/missions` - List all missions
- `GET /api/missions/<id>` - Get specific mission
- `POST /api/missions` - Create new mission
- `PUT /api/missions/<id>` - Update mission
- `DELETE /api/missions/<id>` - Delete mission
- `POST /api/missions/<id>/annotations` - Add annotation to mission
- `POST /api/missions/<id>/no_fly_zones` - Add no-fly zone to mission

## API Response Format

All API responses follow a standardized format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "timestamp": "2025-09-26T20:10:00Z",
  "request_id": "abc12345",
  "meta": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": 400,
    "details": { ... }
  },
  "timestamp": "2025-09-26T20:10:00Z",
  "request_id": "abc12345"
}
```

## Security Features

- **CORS**: Configured for frontend integration
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP, etc.
- **Request Validation**: JSON schema validation for API requests
- **Error Handling**: Secure error responses without sensitive information exposure

## Logging

The application uses structured logging with:
- **Console Output**: For development debugging
- **File Logging**: Rotating log files in `logs/` directory
- **Error Logging**: Separate error log file
- **Request Logging**: HTTP request/response logging

Log files:
- `logs/app.log` - General application logs
- `logs/errors.log` - Error-specific logs

## Database

Uses SQLAlchemy ORM with support for:
- **SQLite**: Default for development
- **PostgreSQL/MySQL**: Production-ready options
- **Migrations**: Ready for Flask-Migrate integration

### Models
- **Mission**: Core mission data with KML content
- **Annotation**: Point annotations on missions
- **NoFlyZone**: Polygon no-fly zones for missions

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python init_db.py
   ```

3. **Run Application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## Development

### Adding New Endpoints
1. Create route functions in `app/routes/`
2. Use `api_response()` and `api_error_response()` for consistent responses
3. Add proper error handling with try-catch blocks
4. Register blueprints in `app/__init__.py`

### Error Handling
Use custom exceptions from `app.errors`:
- `ValidationError` - For request validation failures
- `NotFoundError` - For missing resources
- `ConflictError` - For state conflicts

### Logging
```python
from flask import current_app
current_app.logger.info("Your message here")
```

## Production Deployment

1. Set `FLASK_ENV=production`
2. Configure proper `SECRET_KEY`
3. Use production database (PostgreSQL recommended)
4. Set up reverse proxy (nginx)
5. Use WSGI server (gunicorn)
6. Configure log rotation
7. Set up monitoring for health endpoints

## Testing

The application is ready for testing with:
- Separate testing configuration
- In-memory database for tests
- Error handler testing
- API endpoint testing

## Next Steps

This foundation provides:
- ✅ Solid REST API infrastructure
- ✅ Production-ready error handling
- ✅ Comprehensive logging
- ✅ Security middleware
- ✅ Standardized responses
- ✅ Health monitoring

Ready for:
- Data model refinement
- Business logic implementation
- Input validation rules
- Authentication/authorization
- API documentation (OpenAPI/Swagger)
- Automated testing
- CI/CD pipeline integration
