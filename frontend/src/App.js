import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header.tsx';
import Map from './components/Map.tsx';
import Modal from './components/Modal.tsx';
import FileUpload from './components/FileUpload.tsx';
import MissionTabBar from './components/MissionTabBar.tsx';
import { getAllMissions } from './services/missionService.ts';

function App() {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [missions, setMissions] = useState([]);
  const [activeMissionId, setActiveMissionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

 const loadMissions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAllMissions();
      
      if (response.success) {
        // Store full mission data including waypoints
        setMissions(response.data);
        
        // Set first mission as active if no active mission and missions exist
        if (response.data.length > 0 && !activeMissionId) {
          setActiveMissionId(response.data[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load missions:', err);
      setError('Failed to load missions');
    } finally {
      setLoading(false);
    }
  };

  // Load missions on component mount
  useEffect(() => {
    loadMissions();
  }, []);

  const handleUploadClick = () => {
    setIsUploadModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsUploadModalOpen(false);
  };

  const handleUploadSuccess = (mission, waypoints) => {
    console.log('Upload successful:', { mission, waypoints });
    
    // Add new mission to the list and set it as active
    const newMission = {
      id: mission.id,
      name: mission.name,
      waypoints: waypoints,
      waypoint_count: waypoints.length,
      annotations: [],
      no_fly_zones: []
    };
    setMissions(prev => [...prev, newMission]);
    setActiveMissionId(mission.id);
    
    // Close modal after short delay
    setTimeout(() => {
      setIsUploadModalOpen(false);
    }, 2000);
  };

  const handleMissionSelect = (missionId) => {
    setActiveMissionId(missionId);
    console.log('Selected mission:', missionId);
  };

  // Get active mission's waypoints
  const activeMission = missions.find(mission => mission.id === activeMissionId);
  const activeWaypoints = activeMission ? activeMission.waypoints : [];

  return (
    <div className="App">
      <Header />
      
      <MissionTabBar
        missions={missions}
        activeMissionId={activeMissionId}
        onMissionSelect={handleMissionSelect}
        onUploadClick={handleUploadClick}
        loading={loading}
      />
      
      <main className="main-content">
        <Map waypoints={activeWaypoints} />
      </main>

      <Modal 
        isOpen={isUploadModalOpen} 
        onClose={handleCloseModal}
        title="Upload Mission File"
      >
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      </Modal>
    </div>
  );
}

export default App;
