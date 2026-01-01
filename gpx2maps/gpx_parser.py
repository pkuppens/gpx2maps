"""
GPX file parser using gpxpy
"""

import gpxpy
import gpxpy.gpx
from typing import Dict, List, Tuple


class GPXParser:
    """Parse GPX files and extract route information"""
    
    def __init__(self, gpx_file: str):
        """Initialize parser with GPX file path"""
        self.gpx_file = gpx_file
        self.gpx = None
    
    def parse(self) -> Dict:
        """Parse GPX file and return route data"""
        with open(self.gpx_file, 'r') as f:
            self.gpx = gpxpy.parse(f)
        
        # Extract route data
        route_data = {
            'name': self._get_name(),
            'description': self._get_description(),
            'points': self._get_points(),
            'waypoints': self._get_waypoints(),
            'distance': self._calculate_distance(),
            'elevation_gain': self._calculate_elevation_gain(),
            'bounds': self._get_bounds(),
        }
        
        return route_data
    
    def _get_name(self) -> str:
        """Get route name from GPX file"""
        if self.gpx.name:
            return self.gpx.name
        
        # Try to get name from first track
        if self.gpx.tracks:
            return self.gpx.tracks[0].name or 'Unnamed Route'
        
        # Try to get name from metadata
        if self.gpx.metadata and hasattr(self.gpx.metadata, 'name'):
            return self.gpx.metadata.name
        
        return 'Unnamed Route'
    
    def _get_description(self) -> str:
        """Get route description from GPX file"""
        if self.gpx.description:
            return self.gpx.description
        
        if self.gpx.tracks and self.gpx.tracks[0].description:
            return self.gpx.tracks[0].description
        
        if self.gpx.metadata and hasattr(self.gpx.metadata, 'description'):
            return self.gpx.metadata.description
        
        return ''
    
    def _get_points(self) -> List[Tuple[float, float]]:
        """Extract all track points as (lat, lon) tuples"""
        points = []
        
        # Extract from tracks
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        
        # If no tracks, extract from routes
        if not points:
            for route in self.gpx.routes:
                for point in route.points:
                    points.append((point.latitude, point.longitude))
        
        return points
    
    def _get_waypoints(self) -> List[Dict]:
        """Extract waypoints with metadata"""
        waypoints = []
        
        for waypoint in self.gpx.waypoints:
            waypoints.append({
                'lat': waypoint.latitude,
                'lon': waypoint.longitude,
                'name': waypoint.name or '',
                'description': waypoint.description or '',
                'elevation': waypoint.elevation,
            })
        
        return waypoints
    
    def _calculate_distance(self) -> float:
        """Calculate total distance in kilometers"""
        total_distance = 0.0
        
        # Calculate distance from tracks
        for track in self.gpx.tracks:
            total_distance += track.length_3d() if track.length_3d() else track.length_2d()
        
        # If no tracks, calculate from routes
        if total_distance == 0:
            for route in self.gpx.routes:
                total_distance += route.length_3d() if route.length_3d() else route.length_2d()
        
        # Convert meters to kilometers
        return total_distance / 1000.0
    
    def _calculate_elevation_gain(self) -> float:
        """Calculate total elevation gain in meters"""
        uphill = 0.0
        
        for track in self.gpx.tracks:
            uphill_downhill = track.get_uphill_downhill()
            if uphill_downhill:
                uphill += uphill_downhill.uphill
        
        if uphill == 0:
            for route in self.gpx.routes:
                uphill_downhill = route.get_uphill_downhill()
                if uphill_downhill:
                    uphill += uphill_downhill.uphill
        
        return uphill
    
    def _get_bounds(self) -> Dict:
        """Get bounding box of the route"""
        bounds = self.gpx.get_bounds()
        
        if bounds:
            return {
                'min_lat': bounds.min_latitude,
                'max_lat': bounds.max_latitude,
                'min_lon': bounds.min_longitude,
                'max_lon': bounds.max_longitude,
            }
        
        return {}
