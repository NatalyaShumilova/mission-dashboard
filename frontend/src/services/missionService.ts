// API service for mission-related operations

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// Types
export interface Waypoint {
  id: number;
  mission_id: number;
  latitude: number;
  longitude: number;
  altitude: number | null;
  index: number;
}

export interface Mission {
  id: number;
  name: string;
  waypoints?: Waypoint[];
  waypoint_count?: number;
  annotations?: any[];
  no_fly_zones?: any[];
}

export interface MissionResponse {
  success: boolean;
  data: {
    mission: Mission;
    waypoints: Waypoint[];
    waypoint_count: number;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface AnnotationData {
  latitude: number;
  longitude: number;
  note?: string;
}

export interface NoFlyZoneData {
  coordinates: string;
  note?: string;
}

/**
 * Upload KML file and create a new mission
 */
export const uploadKMLFile = async (file: File, missionName: string): Promise<MissionResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', missionName);

  const response = await fetch(`${API_BASE_URL}/missions`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Get all missions
 */
export const getAllMissions = async (): Promise<ApiResponse<Mission[]>> => {
  const response = await fetch(`${API_BASE_URL}/missions`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};


/**
 * Create an annotation for a mission
 * TODO: Future feature - implement annotation functionality
 */
export const createAnnotation = async (
  missionId: number, 
  annotationData: AnnotationData
): Promise<ApiResponse<any>> => {
  const response = await fetch(`${API_BASE_URL}/missions/${missionId}/annotations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(annotationData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Create a no-fly zone for a mission
 * TODO: Future feature - implement no-fly zone functionality
 */
export const createNoFlyZone = async (
  missionId: number, 
  noFlyZoneData: NoFlyZoneData
): Promise<ApiResponse<any>> => {
  const response = await fetch(`${API_BASE_URL}/missions/${missionId}/no_fly_zones`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(noFlyZoneData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};
