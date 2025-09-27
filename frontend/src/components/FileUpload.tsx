import React, { useState } from 'react';
import { uploadKMLFile, Waypoint, Mission } from '../services/missionService.ts';
import './FileUpload.scss';

interface FileUploadProps {
  onUploadSuccess?: (mission: Mission, waypoints: Waypoint[]) => void;
}

interface FileUploadState {
  file: File | null;
  missionName: string;
  waypoints: Waypoint[];
  mission: Mission | null;
  loading: boolean;
  error: string | null;
  success: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [state, setState] = useState<FileUploadState>({
    file: null,
    missionName: '',
    waypoints: [],
    mission: null,
    loading: false,
    error: null,
    success: false,
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setState(prev => ({
      ...prev,
      file: selectedFile,
      error: null,
      success: false,
      waypoints: [],
      mission: null,
    }));
  };

  const handleMissionNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState(prev => ({
      ...prev,
      missionName: event.target.value,
      error: null,
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!state.file) {
      setState(prev => ({ ...prev, error: 'Please select a KML file' }));
      return;
    }

    if (!state.missionName.trim()) {
      setState(prev => ({ ...prev, error: 'Please enter a mission name' }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await uploadKMLFile(state.file, state.missionName.trim());
      
      setState(prev => ({
        ...prev,
        loading: false,
        success: true,
        waypoints: response.data.waypoints,
        mission: response.data.mission,
        error: null,
      }));

      // Notify parent component of successful upload
      if (onUploadSuccess) {
        onUploadSuccess(response.data.mission, response.data.waypoints);
      }

      console.log('Mission created successfully:', response.data);
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to upload KML file',
      }));
    }
  };

  const resetForm = () => {
    setState({
      file: null,
      missionName: '',
      waypoints: [],
      mission: null,
      loading: false,
      error: null,
      success: false,
    });
  };

  //TODO: Rework css classes to avoid so much dependency on class names for each element
  // eg, file-upload__title can instead be an h2 inside file-upload
  return (
    <div className="file-upload">
      <h2 className="file-upload__title">Upload KML Mission File</h2>
      
      <form onSubmit={handleSubmit} className="file-upload__form">
        <div className="file-upload__field">
          <label htmlFor="missionName">Mission Name:</label>
          <input
            type="text"
            id="missionName"
            value={state.missionName}
            onChange={handleMissionNameChange}
            placeholder="Enter mission name"
            disabled={state.loading}
          />
        </div>

        <div className="file-upload__field">
          <label htmlFor="kmlFile">KML File:</label>
          <input
            type="file"
            id="kmlFile"
            accept=".kml"
            onChange={handleFileChange}
            disabled={state.loading}
          />
        </div>

        <button
          type="submit"
          disabled={state.loading || !state.file || !state.missionName.trim()}
          className="file-upload__submit-btn"
        >
          {state.loading ? 'Uploading...' : 'Upload Mission'}
        </button>
      </form>

      {state.error && (
        <div className="file-upload__alert file-upload__alert--error">
          <strong>Error:</strong> {state.error}
        </div>
      )}

      {state.success && state.mission && (
        <div className="file-upload__alert file-upload__alert--success">
          <strong>Success!</strong> Mission "{state.mission.name}" created successfully with ID: {state.mission.id}
          <div className="file-upload__success-actions">
            <button onClick={resetForm}>
              Upload Another Mission
            </button>
          </div>
        </div>
      )}

      {state.waypoints.length > 0 && (
        <div className="file-upload__waypoints">
          <h3 className="file-upload__waypoints-title">
            Extracted Waypoints ({state.waypoints.length})
          </h3>
          <div className="file-upload__waypoints-container">
            {state.waypoints.map((waypoint, index) => (
              <div key={index} className="file-upload__waypoints-item">
                <strong>Waypoint {waypoint.index}:</strong>
                <div className="coordinates">
                  Lat: {waypoint.latitude.toFixed(6)}, 
                  Lng: {waypoint.longitude.toFixed(6)}
                  {waypoint.altitude && (
                    <span>, Alt: {waypoint.altitude.toFixed(2)}m</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
