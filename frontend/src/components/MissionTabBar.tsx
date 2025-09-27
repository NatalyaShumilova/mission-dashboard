import React from 'react';
import './MissionTabBar.scss';

export interface Mission {
  id: number;
  name: string;
}

interface MissionTabBarProps {
  missions: Mission[];
  activeMissionId: number | null;
  onMissionSelect: (missionId: number) => void;
  onUploadClick: () => void;
  loading?: boolean;
}

const MissionTabBar: React.FC<MissionTabBarProps> = ({
  missions,
  activeMissionId,
  onMissionSelect,
  onUploadClick,
  loading = false
}) => {
  return (
    <div className="mission-tab-bar">
      <div className="mission-tab-bar__container">
        {loading ? (
          <div className="mission-tab-bar__loading">
            <div className="mission-tab-bar__loading-spinner"></div>
            <span>Loading missions...</span>
          </div>
        ) : (
          <>
            {missions.map((mission) => (
              <button
                key={mission.id}
                className={`mission-tab ${
                  activeMissionId === mission.id ? 'mission-tab--active' : ''
                }`}
                onClick={() => onMissionSelect(mission.id)}
                title={`${mission.name}`}
              >
                <span className="mission-tab__name">{mission.name}</span>
              </button>
            ))}
            
            <button
              className="mission-tab mission-tab--upload"
              onClick={onUploadClick}
              title="Upload new mission"
            >
              <span className="mission-tab__upload-icon">+</span>
              <span className="mission-tab__name">Upload Mission</span>
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default MissionTabBar;
