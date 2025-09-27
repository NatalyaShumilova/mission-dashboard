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
        const missionList = response.data.map(mission => ({
          id: mission.id,
          name: mission.name
        }));
        setMissions(missionList);
        
        // Set first mission as active if no active mission and missions exist
        if (missionList.length > 0 && !activeMissionId) {
          setActiveMissionId(missionList[0].id);
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
      name: mission.name
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
    // TODO: In future, this will update the map to show the selected mission's waypoints
    console.log('Selected mission:', missionId);
  };

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
        <Map />
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
