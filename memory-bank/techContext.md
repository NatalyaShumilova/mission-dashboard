# Tech Context

## Technology Stack
- **Frontend**: React
- **Backend**: Python (Flask) with production-ready infrastructure
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Map Component**: Mapbox
- **Architecture**: Application Factory Pattern with Blueprint organization

## Development Setup

### Backend Setup (Production-Ready)
- **Application Structure**: Modular Flask application with application factory pattern
- **Configuration Management**: Environment-specific configuration classes
- **Database**: SQLAlchemy ORM with migration support
- **Error Handling**: Custom exception classes with standardized error responses
- **Logging**: Structured logging with file rotation and multiple log levels
- **Security**: CORS configuration, security headers, input validation
- **Monitoring**: Health check endpoints and request tracking

### Frontend Setup
- Initialize a React project using Create React App
- Install necessary dependencies (e.g., Mapbox GL JS)
- Configure API client for backend communication

### Database Setup
- **Development**: SQLite with automatic initialization
- **Production**: PostgreSQL/MySQL with connection pooling
- **ORM**: SQLAlchemy with relationship mapping
- **Migrations**: Ready for Flask-Migrate integration

### Mapbox Integration
- Set up Mapbox account and obtain API key
- Integrate Mapbox GL JS into the React project
- Configure map component to render flight paths and annotations

## Dependencies

### Backend Dependencies (Production-Ready)
```
Flask==3.1.2                 # Web framework
flask-cors==6.0.1            # CORS handling
Flask-SQLAlchemy==3.1.1      # Database ORM
python-dotenv==1.1.1         # Environment variable management
SQLAlchemy==2.0.43           # Database toolkit
Werkzeug==3.1.3              # WSGI utilities
```

### Additional Production Dependencies (Recommended)
```
gunicorn                     # WSGI server for production
Flask-Migrate               # Database migrations
marshmallow                 # Data validation and serialization
Flask-Limiter               # Rate limiting
psycopg2-binary            # PostgreSQL adapter
```

### Frontend Dependencies
- React, Mapbox GL JS, Axios (for API calls)

## Infrastructure Components

### Application Factory
- Environment-specific configuration loading
- Extension initialization (database, CORS, etc.)
- Blueprint registration
- Error handler registration
- Middleware setup

### Error Handling System
- Custom exception classes (`APIError`, `ValidationError`, `NotFoundError`)
- Global error handlers with proper HTTP status codes
- Standardized error response format
- Comprehensive error logging

### Logging Infrastructure
- **Console Logging**: Development debugging
- **File Logging**: Rotating log files (`logs/app.log`)
- **Error Logging**: Separate error log file (`logs/errors.log`)
- **Request Logging**: HTTP request/response tracking
- **Structured Format**: Consistent log formatting with timestamps

### Security Framework
- **CORS Configuration**: Specific origins and methods
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP, HSTS
- **Input Validation**: Request data validation and sanitization
- **Error Information**: Secure error responses without sensitive data exposure

### API Response Framework
- **Standardized Format**: Success/error indicators with metadata
- **Request Tracking**: Unique request IDs for debugging
- **Timestamp Inclusion**: UTC timestamps for all responses
- **Pagination Support**: Built-in pagination utilities
- **Response Headers**: Processing time and API version headers

### Monitoring & Health Checks
- **Health Endpoint**: `/health` for basic service status
- **Readiness Endpoint**: `/health/ready` with database connectivity check
- **Request Timing**: Processing time measurement and logging
- **API Versioning**: Version header support

## Tool Usage Patterns
- **Backend**: Use pip for dependency management, Flask CLI for development
- **Frontend**: Use npm for managing frontend dependencies
- **Database**: SQLAlchemy CLI for database operations
- **Development**: Environment variables for configuration
- **Production**: WSGI server (gunicorn) with reverse proxy (nginx)

## Development Workflow
1. **Environment Setup**: Load configuration from environment variables
2. **Database Initialization**: Run `python init_db.py` to create tables
3. **Development Server**: Run `python run.py` for development
4. **API Testing**: Use health endpoints to verify service status
5. **Logging**: Monitor `logs/` directory for application logs
6. **Error Debugging**: Check error logs and request IDs for troubleshooting

## Production Deployment Considerations
- **Configuration**: Use production configuration class
- **Database**: PostgreSQL with connection pooling
- **WSGI Server**: Gunicorn with multiple workers
- **Reverse Proxy**: Nginx for static files and load balancing
- **Logging**: Centralized logging with log aggregation
- **Monitoring**: Health check integration with monitoring systems
- **Security**: HTTPS, proper secret management, security headers
