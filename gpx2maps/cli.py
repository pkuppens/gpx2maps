#!/usr/bin/env python3
"""
CLI tool to scrape GPX walking routes from Belgian hiking websites and convert to Google Maps
"""

import argparse
import sys
from typing import Optional
from .scraper import RouteYouScraper, WikilocScraper
from .gpx_parser import GPXParser
from .maps_converter import MapsConverter


def main():
    """Main entry point for the CLI tool"""
    parser = argparse.ArgumentParser(
        description='Scrape GPX routes and convert them to Google Maps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for routes in Malmedy area
  gpx2maps search --location Malmedy --distance 10

  # Download a specific route by URL
  gpx2maps download --url https://www.routeyou.com/route/view/12345

  # Convert a local GPX file to Google Maps
  gpx2maps convert route.gpx --api-key YOUR_API_KEY
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for routes')
    search_parser.add_argument('--location', default='Malmedy', help='Location to search (default: Malmedy)')
    search_parser.add_argument('--distance', type=float, default=10, help='Distance in km (default: 10)')
    search_parser.add_argument('--source', choices=['routeyou', 'wikiloc', 'all'], default='all',
                               help='Source website (default: all)')
    search_parser.add_argument('--prefix', default='MDY', help='Route prefix filter (default: MDY)')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download GPX file from URL')
    download_parser.add_argument('--url', required=True, help='URL of the route')
    download_parser.add_argument('--output', help='Output filename (default: auto-generated)')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert GPX to Google Maps')
    convert_parser.add_argument('gpx_file', help='Path to GPX file')
    convert_parser.add_argument('--api-key', help='Google Maps API key (RECOMMENDED: use GOOGLE_MAPS_API_KEY env var instead for security)')
    convert_parser.add_argument('--output', help='Output file for the Google Maps link')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List downloaded GPX files')
    list_parser.add_argument('--directory', default='gpx_files', help='Directory containing GPX files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'search':
            return search_routes(args)
        elif args.command == 'download':
            return download_route(args)
        elif args.command == 'convert':
            return convert_to_maps(args)
        elif args.command == 'list':
            return list_routes(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def search_routes(args):
    """Search for routes"""
    print(f"🔍 Searching for routes near {args.location} within {args.distance}km...")
    print(f"   Filtering for routes with prefix: {args.prefix}")
    
    sources = []
    if args.source in ['routeyou', 'all']:
        sources.append(('RouteYou', RouteYouScraper()))
    if args.source in ['wikiloc', 'all']:
        sources.append(('Wikiloc', WikilocScraper()))
    
    all_routes = []
    for name, scraper in sources:
        print(f"\n📡 Searching {name}...")
        try:
            routes = scraper.search(args.location, args.distance, args.prefix)
            all_routes.extend(routes)
            print(f"   Found {len(routes)} routes on {name}")
        except Exception as e:
            print(f"   ⚠️  Error searching {name}: {e}")
    
    if not all_routes:
        print("\n❌ No routes found")
        return 1
    
    print(f"\n✅ Found {len(all_routes)} total routes:\n")
    for i, route in enumerate(all_routes, 1):
        print(f"{i}. {route['title']}")
        print(f"   Distance: {route.get('distance', 'N/A')} km")
        print(f"   URL: {route['url']}")
        print()
    
    return 0


def download_route(args):
    """Download a GPX file from URL"""
    from urllib.parse import urlparse
    
    print(f"⬇️  Downloading route from {args.url}...")
    
    # Determine scraper based on URL hostname
    try:
        parsed_url = urlparse(args.url)
        hostname = parsed_url.netloc.lower()
        
        # Check if hostname ends with the expected domain to prevent subdomain attacks
        if hostname.endswith('routeyou.com') or hostname == 'routeyou.com':
            scraper = RouteYouScraper()
        elif hostname.endswith('wikiloc.com') or hostname == 'wikiloc.com':
            scraper = WikilocScraper()
        else:
            print("❌ Unsupported URL. Please use RouteYou or Wikiloc URLs.")
            return 1
    except Exception:
        print("❌ Invalid URL format.")
        return 1
    
    try:
        filename = scraper.download(args.url, args.output)
        print(f"✅ Downloaded to: {filename}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def convert_to_maps(args):
    """Convert GPX file to Google Maps"""
    import os
    
    api_key = args.api_key or os.environ.get('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: Google Maps API key required.")
        print("   RECOMMENDED: Set GOOGLE_MAPS_API_KEY environment variable")
        print("   Alternative: Use --api-key flag (less secure)")
        return 1
    
    print(f"📂 Parsing GPX file: {args.gpx_file}...")
    
    try:
        parser = GPXParser(args.gpx_file)
        route_data = parser.parse()
        
        print(f"   Route: {route_data['name']}")
        print(f"   Points: {len(route_data['points'])}")
        print(f"   Distance: {route_data['distance']:.2f} km")
        
        print(f"\n🗺️  Converting to Google Maps...")
        converter = MapsConverter(api_key)
        maps_url = converter.convert(route_data)
        
        print(f"\n✅ Google Maps link:")
        print(f"   {maps_url}")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(maps_url + '\n')
            print(f"\n💾 Saved to: {args.output}")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def list_routes(args):
    """List downloaded GPX files"""
    import os
    import glob
    
    directory = args.directory
    if not os.path.exists(directory):
        print(f"📁 Directory '{directory}' not found")
        return 1
    
    gpx_files = glob.glob(os.path.join(directory, '*.gpx'))
    
    if not gpx_files:
        print(f"📁 No GPX files found in '{directory}'")
        return 0
    
    print(f"📁 GPX files in '{directory}':\n")
    for gpx_file in sorted(gpx_files):
        try:
            parser = GPXParser(gpx_file)
            route_data = parser.parse()
            print(f"• {os.path.basename(gpx_file)}")
            print(f"  Name: {route_data['name']}")
            print(f"  Distance: {route_data['distance']:.2f} km")
            print(f"  Points: {len(route_data['points'])}")
            print()
        except Exception as e:
            print(f"• {os.path.basename(gpx_file)} (Error: {e})")
            print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
