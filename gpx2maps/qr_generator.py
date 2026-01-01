"""
Generate QR codes for Google Maps routes
"""

import qrcode
from typing import Dict, List, Tuple
from PIL import Image


def create_maps_url_no_api(points: List[Tuple[float, float]], route_name: str = "Route") -> str:
    """
    Create a Google Maps directions URL without requiring an API key.
    
    Uses the Google Maps directions URL format which works without authentication.
    The URL will open in Google Maps app on Android when scanned.
    
    Args:
        points: List of (latitude, longitude) tuples
        route_name: Name of the route (for reference, not used in URL)
    
    Returns:
        Google Maps URL string
    """
    if not points:
        raise ValueError("No points provided")
    
    # Simplify points if too many (Google Maps URLs have length limits)
    # Use up to 25 waypoints for best compatibility
    max_points = 25
    if len(points) > max_points:
        simplified = [points[0]]  # Always include start
        step = len(points) // (max_points - 2)
        for i in range(step, len(points) - 1, step):
            simplified.append(points[i])
        simplified.append(points[-1])  # Always include end
        points = simplified
    
    # Create directions URL format: /dir/point1/point2/.../pointN
    path_segments = [f"{lat},{lon}" for lat, lon in points]
    base_url = "https://www.google.com/maps/dir"
    url = f"{base_url}/{'/'.join(path_segments)}"
    
    # Add walking mode parameter (3e2 = walking/pedestrian)
    # Format: /@center_lat,center_lon,zoom/data=!4m2!4m1!3e2
    center_lat = points[0][0]
    center_lon = points[0][1]
    zoom = 13
    url += f"/@{center_lat},{center_lon},{zoom}z/data=!4m2!4m1!3e2"
    
    return url


def generate_qr_code(url: str, output_path: str, size: int = 10, border: int = 4) -> str:
    """
    Generate a QR code image from a URL.
    
    Args:
        url: URL to encode in the QR code
        output_path: Path where to save the QR code image
        size: Box size for QR code (larger = bigger image)
        border: Border size in boxes
    
    Returns:
        Path to the saved QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path


def create_route_qr_code(route_data: Dict, output_path: str = None) -> Tuple[str, str]:
    """
    Create a QR code for a GPX route that opens in Google Maps.
    
    Works without Google Maps API key by using the public directions URL format.
    
    Args:
        route_data: Dictionary with 'points' and optionally 'name'
        output_path: Optional output path for QR code (default: auto-generated)
    
    Returns:
        Tuple of (maps_url, qr_code_path)
    """
    points = route_data.get('points', [])
    if not points:
        raise ValueError("No points found in route data")
    
    route_name = route_data.get('name', 'Route')
    
    # Create Google Maps URL without API key
    maps_url = create_maps_url_no_api(points, route_name)
    
    # Generate output filename if not provided
    if not output_path:
        import os
        route_id = route_data.get('name', 'route').replace(' ', '_').lower()
        output_path = f"qr_{route_id}.png"
    
    # Generate QR code
    qr_path = generate_qr_code(maps_url, output_path)
    
    return maps_url, qr_path

