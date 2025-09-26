# System Patterns

## Architecture Overview
The Drone Mission Planning Dashboard will follow a client-server architecture with the following components:

1. **Frontend (Client)**
   - Built with React
   - Responsible for user interface and user interactions
   - Communicates with the backend via REST API

2. **Backend (Server)**
   - Built with Python (Flask or Django)
   - Handles business logic and data storage
   - Provides REST API for frontend communication

3. **Database**
   - Uses persistent storage (e.g., SQLite for local development)
   - Stores mission data, annotations, and no-fly zones

4. **Map Component**
   - Uses Mapbox for rendering maps and flight paths

## Design Patterns
- **Model-View-Controller (MVC)** for separating concerns in the frontend
- **RESTful API** for communication between frontend and backend
- **Singleton** for managing the map instance
- **Observer** pattern for real-time updates (stretch goal)

## Component Relationships
- The frontend communicates with the backend via REST API
- The backend interacts with the database to store and retrieve data
- The map component is integrated into the frontend and communicates with the backend for data

## Critical Implementation Paths
1. **File Upload**: Frontend to Backend (KML file processing)
2. **Data Rendering**: Backend to Frontend (mission data, annotations, no-fly zones)
3. **Real-time Updates**: Frontend to Backend (annotations, no-fly zones)
