import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Map from './components/Map';
import Modal from './components/Modal';
import FileUpload from './components/FileUpload';
import MissionTabBar from './components/MissionTabBar';
import { getAllMissions, Mission, Waypoint } from './services/missionService';

const App: React.FC = () => {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState<boolean>(false);
  const [missions, setMissions] = useState<Mission[]>([]);
  const [activeMissionId, setActiveMissionId] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadMissions = async (): Promise<void> => {
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

  const handleUploadClick = (): void => {
    setIsUploadModalOpen(true);
  };

  const handleCloseModal = (): void => {
    setIsUploadModalOpen(false);
  };

  const handleUploadSuccess = (mission: Mission, waypoints: Waypoint[]): void => {
    console.log('Upload successful:', { mission, waypoints });
    
    // Add new mission to the list and set it as active
    const newMission: Mission = {
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

  const handleMissionSelect = (missionId: number): void => {
    setActiveMissionId(missionId);
    console.log('Selected mission:', missionId);
  };

  // Get active mission's waypoints
  const activeMission = missions.find(mission => mission.id === activeMissionId);
  const activeWaypoints = activeMission?.waypoints || [];

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
};

export default App;
