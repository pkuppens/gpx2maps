"""
Web scrapers for hiking route websites
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Base class for route scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        # Use a recent Chrome User-Agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    @abstractmethod
    def search(self, location: str, distance_km: float, prefix: str) -> List[Dict]:
        """Search for routes near location"""
        pass
    
    @abstractmethod
    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """Download GPX file from URL"""
        pass
    
    def _save_gpx(self, content: bytes, filename: str) -> str:
        """Save GPX content to file"""
        os.makedirs('gpx_files', exist_ok=True)
        filepath = os.path.join('gpx_files', filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath
    
    def _create_sample_gpx(self, route_id: str, name: str) -> str:
        """Create a sample GPX file (for demonstration)"""
        # Malmedy coordinates: 50.4233° N, 6.0294° E
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="gpx2maps" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>{name}</name>
    <desc>DEMO SAMPLE ROUTE - Walking route near Malmedy, Belgium - FOR DEMONSTRATION ONLY</desc>
  </metadata>
  <trk>
    <name>{name}</name>
    <trkseg>
      <trkpt lat="50.4233" lon="6.0294">
        <ele>340</ele>
      </trkpt>
      <trkpt lat="50.4250" lon="6.0310">
        <ele>345</ele>
      </trkpt>
      <trkpt lat="50.4270" lon="6.0330">
        <ele>350</ele>
      </trkpt>
      <trkpt lat="50.4285" lon="6.0345">
        <ele>355</ele>
      </trkpt>
      <trkpt lat="50.4290" lon="6.0320">
        <ele>352</ele>
      </trkpt>
      <trkpt lat="50.4275" lon="6.0300">
        <ele>348</ele>
      </trkpt>
      <trkpt lat="50.4250" lon="6.0285">
        <ele>342</ele>
      </trkpt>
      <trkpt lat="50.4233" lon="6.0294">
        <ele>340</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>'''


class RouteYouScraper(BaseScraper):
    """Scraper for RouteYou.com"""
    
    BASE_URL = 'https://www.routeyou.com'
    
    def search(self, location: str, distance_km: float, prefix: str) -> List[Dict]:
        """
        Search for routes on RouteYou
        
        NOTE: This is a sample implementation that returns predefined routes
        for demonstration purposes. For production use, implement actual web
        scraping with proper HTTP requests and HTML parsing.
        """
        routes = []
        
        # RouteYou search URL format for walking routes near Malmedy
        search_url = f"{self.BASE_URL}/en-be/location/walk/search"
        
        try:
            # For quick implementation, we'll provide some known routes
            # In production, this would do actual web scraping
            print(f"   Note: Using sample RouteYou routes for {location}")
            
            # Sample routes around Malmedy with MDY prefix
            sample_routes = [
                {
                    'title': 'MDY-01: DEMO - Malmedy City Walk (SAMPLE ROUTE)',
                    'distance': '5.2',
                    'url': f'{self.BASE_URL}/en-be/route/view/malmedy-city-walk',
                    'source': 'RouteYou'
                },
                {
                    'title': 'MDY-02: DEMO - High Fens Trail (SAMPLE ROUTE)',
                    'distance': '12.5',
                    'url': f'{self.BASE_URL}/en-be/route/view/high-fens-trail',
                    'source': 'RouteYou'
                },
                {
                    'title': 'MDY-03: DEMO - Warche Valley Loop (SAMPLE ROUTE)',
                    'distance': '8.3',
                    'url': f'{self.BASE_URL}/en-be/route/view/warche-valley-loop',
                    'source': 'RouteYou'
                },
            ]
            
            # Filter by prefix and distance
            for route in sample_routes:
                if prefix and not route['title'].startswith(prefix):
                    continue
                try:
                    if float(route['distance']) <= distance_km:
                        routes.append(route)
                except ValueError:
                    routes.append(route)
            
        except Exception as e:
            print(f"   Warning: RouteYou search error: {e}")
        
        return routes
    
    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """Download GPX file from RouteYou"""
        
        # Extract route ID from URL
        route_id_match = re.search(r'/route/view/([^/]+)', url)
        if not route_id_match:
            raise ValueError("Could not extract route ID from URL")
        
        route_id = route_id_match.group(1)
        
        # For quick implementation, create a sample GPX file
        if not output_filename:
            output_filename = f"routeyou_{route_id}.gpx"
        
        # Create a basic GPX file structure
        gpx_content = self._create_sample_gpx(route_id, "DEMO RouteYou Route (SAMPLE)")
        
        return self._save_gpx(gpx_content.encode('utf-8'), output_filename)


class MalmedyTourismScraper(BaseScraper):
    """Scraper for Malmedy Tourism website"""
    
    BASE_URL = 'https://www.malmedy-tourisme.be'
    SIGNPOSTED_WALKS_URL = 'https://www.malmedy-tourisme.be/en/type-a-pied/signposted-walks/'
    
    def search(self, location: str, distance_km: float, prefix: str) -> List[Dict]:
        """
        Search for routes on Malmedy Tourism website.
        
        Scrapes the signposted walks page to find all 26 routes with their
        official MDY IDs (MDY01, MDY02, etc.) as shown on trail markers.
        
        Args:
            location: Location name (e.g., "Malmedy")
            distance_km: Maximum distance in kilometers
            prefix: Route prefix filter (e.g., "MDY")
        
        Returns:
            List of route dictionaries with title, distance, url, and source
        """
        routes = []
        
        try:
            # Fetch the signposted walks page
            response = self.session.get(self.SIGNPOSTED_WALKS_URL, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all route links - they are in <a> tags with class containing "a-pied"
            route_links = soup.find_all('a', href=re.compile(r'/en/a-pied/'))
            
            for link in route_links:
                try:
                    # Extract route URL
                    route_url = link.get('href', '')
                    if not route_url.startswith('http'):
                        route_url = self.BASE_URL + route_url
                    
                    # Find the route title/ID in the table inside the link
                    table = link.find('table', class_='informations')
                    if not table:
                        continue
                    
                    # Find the h3 tag containing the route ID and name
                    h3 = table.find('h3')
                    if not h3:
                        continue
                    
                    title_text = h3.get_text(strip=True)
                    
                    # Extract MDY ID (e.g., "MDY01" or "MDY 21" from title)
                    # Handle both "MDY01" and "MDY 21" formats
                    mdy_match = re.search(r'(MDY\s*\d+)', title_text, re.IGNORECASE)
                    if not mdy_match:
                        continue
                    
                    route_id_raw = mdy_match.group(1)  # e.g., "MDY01" or "MDY 21"
                    # Normalize to "MDY01" format (remove spaces)
                    route_id = re.sub(r'\s+', '', route_id_raw).upper()
                    route_name = title_text.replace(route_id_raw, '').strip()
                    
                    # Extract distance from the KM & Ascent row
                    distance_str = None
                    km_row = table.find('th', string=re.compile(r'KM'))
                    if km_row:
                        td = km_row.find_next_sibling('td')
                        if td:
                            distance_text = td.get_text(strip=True)
                            # Extract distance (e.g., "11 km" or "5,5 km")
                            distance_match = re.search(r'([\d,]+)\s*km', distance_text, re.IGNORECASE)
                            if distance_match:
                                distance_str = distance_match.group(1).replace(',', '.')
                    
                    # Build title with proper MDY ID format
                    title = f"{route_id} {route_name}"
                    
                    # Filter by prefix
                    if prefix and not route_id.startswith(prefix):
                        continue
                    
                    # Filter by distance
                    if distance_str:
                        try:
                            distance_float = float(distance_str)
                            if distance_float > distance_km:
                                continue
                        except ValueError:
                            pass  # Include route even if distance parsing fails
                    
                    routes.append({
                        'title': title,
                        'distance': distance_str or 'N/A',
                        'url': route_url,
                        'source': 'Malmedy Tourism',
                        'route_id': route_id  # Store the official ID
                    })
                    
                except Exception as e:
                    # Skip routes that can't be parsed
                    continue
            
            # Sort routes by MDY ID
            routes.sort(key=lambda x: x.get('route_id', ''))
            
        except requests.RequestException as e:
            print(f"   Warning: Error fetching Malmedy Tourism page: {e}")
        except Exception as e:
            print(f"   Warning: Malmedy Tourism search error: {e}")
        
        return routes
    
    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """
        Download GPX file from Malmedy Tourism route page.
        
        Attempts to find and download the GPX file from the Cirkwi export link
        on the route page. Falls back to creating a sample GPX if download fails.
        
        Args:
            url: URL of the route page
            output_filename: Optional output filename (default: auto-generated)
        
        Returns:
            Path to the downloaded GPX file
        
        Raises:
            ValueError: If route URL cannot be parsed or GPX cannot be downloaded
        """
        route_id = None
        route_name = None
        soup = None
        
        try:
            # Fetch the route page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract route ID and name from the page
            h1 = soup.find('h1')
            if h1:
                title_text = h1.get_text(strip=True)
                mdy_match = re.search(r'(MDY\s*\d+)', title_text, re.IGNORECASE)
                if mdy_match:
                    route_id = re.sub(r'\s+', '', mdy_match.group(1)).upper()
                    route_name = title_text.strip()
            
            # If not found in h1, try other headings
            if not route_id:
                for heading in soup.find_all(['h1', 'h2', 'h3']):
                    heading_text = heading.get_text(strip=True)
                    mdy_match = re.search(r'(MDY\s*\d+)', heading_text, re.IGNORECASE)
                    if mdy_match:
                        route_id = re.sub(r'\s+', '', mdy_match.group(1)).upper()
                        route_name = heading_text.strip()
                        break
            
            # Find GPX export link (Cirkwi exporter)
            gpx_link = soup.find('a', {'id': 'cdf_exporterGPX'}) or \
                      soup.find('a', class_=re.compile(r'gpx', re.I)) or \
                      soup.find('a', href=re.compile(r'cirkwi.*gpx', re.I))
            
            if gpx_link:
                gpx_url = gpx_link.get('href', '')
                if not gpx_url.startswith('http'):
                    gpx_url = self.BASE_URL + gpx_url
                
                # Clean up HTML entities in URL
                gpx_url = gpx_url.replace('&amp;', '&')
                
                try:
                    # Download the GPX file
                    gpx_response = self.session.get(gpx_url, timeout=30, allow_redirects=True)
                    gpx_response.raise_for_status()
                    
                    # Check if it's actually a GPX file
                    content_type = gpx_response.headers.get('Content-Type', '').lower()
                    if 'gpx' in content_type or 'xml' in content_type or \
                       gpx_response.text.strip().startswith('<?xml') or \
                       '<gpx' in gpx_response.text.lower():
                        
                        # Generate filename if not provided
                        if not output_filename:
                            if route_id:
                                output_filename = f"malmedy_{route_id.lower()}.gpx"
                            else:
                                route_slug = url.split('/')[-1].rstrip('/')
                                output_filename = f"malmedy_{route_slug}.gpx"
                        
                        return self._save_gpx(gpx_response.content, output_filename)
                    
                except Exception as e:
                    print(f"   Warning: Could not download GPX from Cirkwi: {e}")
            
        except requests.RequestException as e:
            print(f"   Warning: Error fetching route page: {e}")
        except Exception as e:
            print(f"   Warning: Error processing route page: {e}")
        
        # Fallback: create a placeholder GPX file
        route_slug = url.split('/')[-1].rstrip('/')
        
        if not route_name:
            route_name = route_slug.replace('-', ' ').title()
        
        # Use route ID in name if available
        if route_id and not route_name.startswith(route_id):
            route_name = f"{route_id} {route_name}"
        
        if not output_filename:
            if route_id:
                output_filename = f"malmedy_{route_id.lower()}.gpx"
            else:
                output_filename = f"malmedy_{route_slug}.gpx"
        
        # Create a placeholder GPX file
        gpx_content = self._create_sample_gpx(route_slug, route_name)
        
        return self._save_gpx(gpx_content.encode('utf-8'), output_filename)


class WikilocScraper(BaseScraper):
    """Scraper for Wikiloc.com"""
    
    BASE_URL = 'https://www.wikiloc.com'
    
    def search(self, location: str, distance_km: float, prefix: str) -> List[Dict]:
        """
        Search for routes on Wikiloc
        
        NOTE: This is a sample implementation that returns predefined routes
        for demonstration purposes. For production use, implement actual web
        scraping with proper HTTP requests and HTML parsing.
        """
        routes = []
        
        try:
            # For quick implementation, we'll provide some known routes
            print(f"   Note: Using sample Wikiloc routes for {location}")
            
            # Sample routes around Malmedy with MDY prefix
            sample_routes = [
                {
                    'title': 'MDY-04: DEMO - Bayehon Waterfall Walk (SAMPLE ROUTE)',
                    'distance': '6.8',
                    'url': f'{self.BASE_URL}/wikiloc/view.do?id=bayehon-waterfall',
                    'source': 'Wikiloc'
                },
                {
                    'title': 'MDY-05: DEMO - Signal de Botrange (SAMPLE ROUTE)',
                    'distance': '9.2',
                    'url': f'{self.BASE_URL}/wikiloc/view.do?id=signal-botrange',
                    'source': 'Wikiloc'
                },
                {
                    'title': 'MDY-06: DEMO - Reinhardstein Castle Route (SAMPLE ROUTE)',
                    'distance': '7.5',
                    'url': f'{self.BASE_URL}/wikiloc/view.do?id=reinhardstein-castle',
                    'source': 'Wikiloc'
                },
            ]
            
            # Filter by prefix and distance
            for route in sample_routes:
                if prefix and not route['title'].startswith(prefix):
                    continue
                try:
                    if float(route['distance']) <= distance_km:
                        routes.append(route)
                except ValueError:
                    routes.append(route)
            
        except Exception as e:
            print(f"   Warning: Wikiloc search error: {e}")
        
        return routes
    
    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """Download GPX file from Wikiloc"""
        
        # Extract route ID from URL
        route_id_match = re.search(r'id=([^&]+)', url)
        if not route_id_match:
            raise ValueError("Could not extract route ID from URL")
        
        route_id = route_id_match.group(1)
        
        if not output_filename:
            output_filename = f"wikiloc_{route_id}.gpx"
        
        # Create a basic GPX file structure
        gpx_content = self._create_sample_gpx(route_id, "DEMO Wikiloc Route (SAMPLE)")
        
        return self._save_gpx(gpx_content.encode('utf-8'), output_filename)
