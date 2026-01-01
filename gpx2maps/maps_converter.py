"""
Convert GPX routes to Google Maps links
"""

import googlemaps
from typing import Dict, List, Tuple
from urllib.parse import urlencode


class MapsConverter:
    """Convert GPX route data to Google Maps"""
    
    # Google Maps URL data parameter for walking mode
    # Format: /@lat,lon,zoom/data=!4m2!4m1!3e2
    # where 3e2 indicates walking/pedestrian mode
    WALKING_MODE_PARAM = "!4m2!4m1!3e2"
    
    # Default zoom level for route display
    DEFAULT_ZOOM = 12
    
    def __init__(self, api_key: str):
        """Initialize converter with Google Maps API key"""
        self.api_key = api_key
        # Only initialize client if it's not a demo key
        self.client = None
        if api_key and api_key != "DEMO_API_KEY":
            try:
                self.client = googlemaps.Client(key=api_key)
            except Exception:
                # If client initialization fails, we'll still generate URLs
                pass
    
    def convert(self, route_data: Dict) -> str:
        """
        Convert route data to a shareable Google Maps link
        
        Args:
            route_data: Dict with 'name', 'points', 'waypoints', etc.
        
        Returns:
            Google Maps URL as string
        """
        points = route_data['points']
        
        if not points:
            raise ValueError("No points found in route data")
        
        # For routes with many points, we need to simplify
        # Google Maps URL has length limits, so we sample points
        simplified_points = self._simplify_points(points, max_points=25)
        
        # Create Google Maps directions URL
        # Format: https://www.google.com/maps/dir/lat1,lon1/lat2,lon2/.../latN,lonN
        maps_url = self._create_maps_url(simplified_points, route_data.get('name', 'Route'))
        
        return maps_url
    
    def _simplify_points(self, points: List[Tuple[float, float]], max_points: int = 25) -> List[Tuple[float, float]]:
        """
        Simplify route by selecting evenly distributed points
        
        Google Maps URLs have length limits, so we need to reduce the number of points
        while preserving the overall route shape.
        """
        if len(points) <= max_points:
            return points
        
        # Always include first and last point
        simplified = [points[0]]
        
        # Calculate step to evenly distribute remaining points
        step = len(points) // (max_points - 1)
        
        for i in range(step, len(points) - 1, step):
            simplified.append(points[i])
        
        # Always include last point
        if simplified[-1] != points[-1]:
            simplified.append(points[-1])
        
        return simplified
    
    def _create_maps_url(self, points: List[Tuple[float, float]], route_name: str) -> str:
        """
        Create a Google Maps directions URL
        
        Format: https://www.google.com/maps/dir/point1/point2/.../pointN
        """
        # Convert points to URL path segments
        path_segments = [f"{lat},{lon}" for lat, lon in points]
        
        # Build the URL
        base_url = "https://www.google.com/maps/dir"
        url = f"{base_url}/{'/'.join(path_segments)}"
        
        # Add data parameter for walking mode
        url += "/@{},{},{}z/data={}".format(
            points[0][0],  # center latitude
            points[0][1],  # center longitude
            self.DEFAULT_ZOOM,
            self.WALKING_MODE_PARAM
        )
        
        return url
    
    def create_static_map_url(self, route_data: Dict, width: int = 600, height: int = 400) -> str:
        """
        Create a static Google Maps image URL showing the route
        
        Args:
            route_data: Dict with 'points' and other route info
            width: Image width in pixels
            height: Image height in pixels
        
        Returns:
            Static Maps API URL
        """
        points = route_data['points']
        
        if not points:
            raise ValueError("No points found in route data")
        
        # Simplify points for path parameter
        simplified_points = self._simplify_points(points, max_points=50)
        
        # Create path parameter
        path_coords = '|'.join([f"{lat},{lon}" for lat, lon in simplified_points])
        
        # Build static map URL
        params = {
            'size': f'{width}x{height}',
            'path': f'color:0x0000ff|weight:3|{path_coords}',
            'key': self.api_key,
        }
        
        base_url = "https://maps.googleapis.com/maps/api/staticmap"
        url = f"{base_url}?{urlencode(params)}"
        
        return url
