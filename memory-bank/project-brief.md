# Drone Mission Planning Dashboard

## Overview
Our customers plan drone missions to capture aerial data (e.g., for construction, agriculture, or inspections). They often need to share planned routes and collaborate with teammates before flying.

## User Story
As a field operations manager, I want to upload a drone mission flight path file (KML), view it on an interactive map, and collaborate with teammates by adding annotations, so that our team can review the mission plan, flag potential hazards, and align before flying.

## Acceptance Criteria
- I can upload a mission file (in KML)
  - Example of a KML exported from a DJI Drone: [KML Example](./example.kml)
- The flight path is rendered on a map
  - Should render each waypoint and the path between them
  - Each waypoint of the mission flight is under the Placemark -> Point -> Coordinates object
  - You are free to ignore any “wpml” prefixed headers, these are DJI specific and not part of the KML spec
- I can add annotation pins anywhere on the map with a short text note.
- I can draw zones (such as polygons) to define no-fly zones with a text note.
- My updates and annotations are saved and persist across sessions.
- The dashboard supports multiple missions, and I can switch between them.
- (Stretch goal) I can see annotations from other users in real-time (without refreshing).

## Technology Requirements
- Frontend must be built using React or Angular
- Backend must be built with Python
- Should use persistent storage such as a database like MongoDB or PostgreSQL
  - Needs to include a way to run it locally (such as a Docker compose file).
  - If not overly familiar, then just use a file based storage such as SQLite
- Must use Mapbox for the map component
- Do not implement auth or user management
