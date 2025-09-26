import React, { useState } from 'react';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [waypoints, setWaypoints] = useState([]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      parseKML(selectedFile);
    }
  };

  const parseKML = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(e.target.result, 'application/xml');
      const placemarks = xmlDoc.getElementsByTagName('Placemark');

      const extractedWaypoints = [];
      for (let i = 0; i < placemarks.length; i++) {
        const coordinates = placemarks[i].getElementsByTagName('coordinates')[0].textContent.trim();
        extractedWaypoints.push(coordinates);
      }

      setWaypoints(extractedWaypoints);
      console.log(extractedWaypoints)
    };
    reader.readAsText(file);
  };

  return (
    <div>
      <h2>Upload KML File</h2>
      <input type="file" accept=".kml" onChange={handleFileChange} />
      {file && <p>Selected file: {file.name}</p>}
      {waypoints.length > 0 && (
        <div>
          <h3>Extracted Waypoints</h3>
          <ul>
            {waypoints.map((wp, index) => (
              <li key={index}>{wp}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
