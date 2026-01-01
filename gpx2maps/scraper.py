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


class MalmedyTourismScraper(BaseScraper):
    """Scraper for Malmedy Tourism website"""
    
    BASE_URL = 'https://www.malmedy-tourisme.be'
    
    def search(self, location: str, distance_km: float, prefix: str) -> List[Dict]:
        """
        Search for routes on Malmedy Tourism website
        
        NOTE: This is a sample implementation that returns predefined routes
        for demonstration purposes. For production use, implement actual web
        scraping of https://www.malmedy-tourisme.be/en/type-a-pied/signposted-walks/
        """
        routes = []
        
        try:
            # For quick implementation, we'll provide some known routes from Malmedy Tourism
            print(f"   Note: Using sample Malmedy Tourism routes for {location}")
            
            # Sample routes from Malmedy Tourism signposted walks
            sample_routes = [
                {
                    'title': 'MDY-07: DEMO - Malmedy Heritage Circuit (SAMPLE ROUTE)',
                    'distance': '4.5',
                    'url': f'{self.BASE_URL}/en/type-a-pied/signposted-walks/heritage-circuit',
                    'source': 'Malmedy Tourism'
                },
                {
                    'title': 'MDY-08: DEMO - Robertville Lake Trail (SAMPLE ROUTE)',
                    'distance': '11.0',
                    'url': f'{self.BASE_URL}/en/type-a-pied/signposted-walks/robertville-lake',
                    'source': 'Malmedy Tourism'
                },
                {
                    'title': 'MDY-09: DEMO - Beverce Valley Walk (SAMPLE ROUTE)',
                    'distance': '7.2',
                    'url': f'{self.BASE_URL}/en/type-a-pied/signposted-walks/beverce-valley',
                    'source': 'Malmedy Tourism'
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
            print(f"   Warning: Malmedy Tourism search error: {e}")
        
        return routes
    
    def download(self, url: str, output_filename: Optional[str] = None) -> str:
        """Download GPX file from Malmedy Tourism"""
        
        # Extract route name from URL
        route_name_match = re.search(r'/signposted-walks/([^/]+)', url)
        if not route_name_match:
            raise ValueError("Could not extract route name from URL")
        
        route_name = route_name_match.group(1)
        
        if not output_filename:
            output_filename = f"malmedy_{route_name}.gpx"
        
        # Create a basic GPX file structure
        gpx_content = self._create_sample_gpx(route_name, "DEMO Malmedy Tourism Route (SAMPLE)")
        
        return self._save_gpx(gpx_content.encode('utf-8'), output_filename)
    
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
    
    def _create_sample_gpx(self, route_id: str, name: str) -> str:
        """Create a sample GPX file (for demonstration)"""
        # Malmedy area coordinates
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="gpx2maps" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>{name}</name>
    <desc>DEMO SAMPLE ROUTE - Walking route near Malmedy, Belgium - FOR DEMONSTRATION ONLY</desc>
  </metadata>
  <trk>
    <name>{name}</name>
    <trkseg>
      <trkpt lat="50.4300" lon="6.0400">
        <ele>360</ele>
      </trkpt>
      <trkpt lat="50.4320" lon="6.0420">
        <ele>365</ele>
      </trkpt>
      <trkpt lat="50.4340" lon="6.0440">
        <ele>370</ele>
      </trkpt>
      <trkpt lat="50.4360" lon="6.0460">
        <ele>375</ele>
      </trkpt>
      <trkpt lat="50.4380" lon="6.0440">
        <ele>372</ele>
      </trkpt>
      <trkpt lat="50.4360" lon="6.0420">
        <ele>368</ele>
      </trkpt>
      <trkpt lat="50.4340" lon="6.0400">
        <ele>363</ele>
      </trkpt>
      <trkpt lat="50.4320" lon="6.0380">
        <ele>358</ele>
      </trkpt>
      <trkpt lat="50.4300" lon="6.0400">
        <ele>360</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>'''
