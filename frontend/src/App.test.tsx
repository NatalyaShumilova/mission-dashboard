import { render, screen, waitFor } from '@testing-library/react';
import App from './App';

// Mock the mission service
const mockGetAllMissions = jest.fn();
jest.mock('./services/missionService', () => ({
  getAllMissions: () => mockGetAllMissions(),
}));

// Mock Mapbox GL JS
jest.mock('mapbox-gl', () => ({
  Map: jest.fn(() => ({
    addControl: jest.fn(),
    on: jest.fn(),
    remove: jest.fn(),
    resize: jest.fn(),
  })),
  NavigationControl: jest.fn(),
  ScaleControl: jest.fn(),
}));

// Mock the custom hooks
jest.mock('./hooks/useMapbox', () => ({
  useMapbox: () => ({
    mapContainer: { current: null },
    map: { current: null },
    mapLoaded: false,
    error: null,
  }),
}));

jest.mock('./hooks/useWaypointVisualization', () => ({
  useWaypointVisualization: () => ({
    updateWaypoints: jest.fn(),
    cleanupWaypoints: jest.fn(),
  }),
}));

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders Mission Dashboard header', () => {
    // Mock successful API call
    mockGetAllMissions.mockResolvedValue({
      success: true,
      data: []
    });

    render(<App />);
    const headerElement = screen.getByText(/Mission Dashboard/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('loads missions on mount', async () => {
    const mockMissions = [
      { id: 1, name: 'Test Mission', waypoints: [], waypoint_count: 0 }
    ];

    mockGetAllMissions.mockResolvedValue({
      success: true,
      data: mockMissions
    });

    render(<App />);

    await waitFor(() => {
      expect(mockGetAllMissions).toHaveBeenCalledTimes(1);
    });
  });

  test('handles mission loading error', async () => {
    mockGetAllMissions.mockRejectedValue(
      new Error('Failed to load missions')
    );

    render(<App />);

    await waitFor(() => {
      expect(mockGetAllMissions).toHaveBeenCalledTimes(1);
    });
  });
});
