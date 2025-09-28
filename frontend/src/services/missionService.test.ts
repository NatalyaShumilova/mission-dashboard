import { uploadKMLFile, getAllMissions } from './missionService';

// Mock fetch globally
global.fetch = jest.fn();

describe('missionService', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  describe('uploadKMLFile', () => {
    test('uploads KML file successfully', async () => {
      const mockResponse = {
        success: true,
        data: {
          mission: { id: 1, name: 'Test Mission' },
          waypoints: [
            { id: 1, mission_id: 1, latitude: 40.7128, longitude: -74.0060, altitude: 100, index: 0 }
          ],
          waypoint_count: 1
        }
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const file = new File(['test content'], 'test.kml', { type: 'application/vnd.google-earth.kml+xml' });
      const result = await uploadKMLFile(file, 'Test Mission');

      expect(fetch).toHaveBeenCalledWith(
        `${process.env.REACT_APP_API_BASE_URL}/missions`,
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData)
        })
      );
      expect(result).toEqual(mockResponse);
    });

    test('handles upload error', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ message: 'Invalid file format' })
      });

      const file = new File(['invalid content'], 'test.txt', { type: 'text/plain' });

      await expect(uploadKMLFile(file, 'Test Mission')).rejects.toThrow('Invalid file format');
    });
  });

  describe('getAllMissions', () => {
    test('fetches all missions successfully', async () => {
      const mockResponse = {
        success: true,
        data: [
          { id: 1, name: 'Mission 1', waypoints: [], waypoint_count: 0 },
          { id: 2, name: 'Mission 2', waypoints: [], waypoint_count: 0 }
        ]
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await getAllMissions();

      expect(fetch).toHaveBeenCalledWith(`${process.env.REACT_APP_API_BASE_URL}/missions`);
      expect(result).toEqual(mockResponse);
    });

    test('handles fetch error', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500
      });

      await expect(getAllMissions()).rejects.toThrow('HTTP error! status: 500');
    });
  });
});
