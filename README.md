# gpx2maps

CLI tool to scrape GPX walking routes from popular Belgian hiking websites (RouteYou, Wikiloc, etc.) for the Malmedy, Belgium area and convert them to Google Maps routes.

## Features

- 🔍 Search for walking routes near Malmedy (MDY prefixed routes)
- ⬇️ Download GPX files from RouteYou and Wikiloc
- 📊 Parse GPX waypoints, tracks, and route metadata
- 🗺️ Convert GPX tracks to shareable Google Maps links
- 📍 Filter routes by location and distance
- ⚡ Progress indicators and error handling

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install uv if you haven't already
pip install uv

# Clone the repository
git clone https://github.com/pkuppens/gpx2maps.git
cd gpx2maps

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
uv pip install -e .
```

### Using pip (Alternative)

```bash
# Clone the repository
git clone https://github.com/pkuppens/gpx2maps.git
cd gpx2maps

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Requirements

- Python 3.7+
- Google Maps API key (for conversion feature) - See [API_KEY_GUIDE.md](API_KEY_GUIDE.md) for setup instructions
- uv (recommended) or pip for package management

## Usage

### Search for Routes

Search for walking routes near Malmedy within 10km:

```bash
gpx2maps search --location Malmedy --distance 10
```

Search only RouteYou:

```bash
gpx2maps search --location Malmedy --distance 10 --source routeyou
```

Filter by prefix (default: MDY):

```bash
gpx2maps search --location Malmedy --distance 10 --prefix MDY
```

### Download GPX Files

Download a route from RouteYou or Wikiloc:

```bash
gpx2maps download --url https://www.routeyou.com/route/view/12345
gpx2maps download --url https://www.wikiloc.com/wikiloc/view.do?id=route-name
```

Save with custom filename:

```bash
gpx2maps download --url https://www.routeyou.com/route/view/12345 --output my-route.gpx
```

### Convert GPX to Google Maps

Convert a GPX file to a Google Maps link:

```bash
# Set your Google Maps API key (see API_KEY_GUIDE.md for detailed setup)
export GOOGLE_MAPS_API_KEY="your-api-key-here"

# Convert the GPX file
gpx2maps convert route.gpx

# Or specify the API key directly (not recommended for security)
gpx2maps convert route.gpx --api-key YOUR_API_KEY

# Save the link to a file
gpx2maps convert route.gpx --output maps-link.txt
```

**Important**: See [API_KEY_GUIDE.md](API_KEY_GUIDE.md) for complete instructions on obtaining and safely using your Google Maps API key.

### List Downloaded Routes

List all GPX files in the gpx_files directory:

```bash
gpx2maps list
```

List from a custom directory:

```bash
gpx2maps list --directory /path/to/gpx/files
```

## Google Maps API Key

To use the conversion feature, you need a Google Maps API key.

**See [API_KEY_GUIDE.md](API_KEY_GUIDE.md) for complete step-by-step instructions** on:
- How to create a Google Cloud project
- How to enable required APIs
- How to generate and restrict your API key
- How to safely use the key with environment variables
- Security best practices
- Pricing and quotas

Quick setup:
```bash
export GOOGLE_MAPS_API_KEY="your-api-key-here"
```

## Project Structure

```
gpx2maps/
├── gpx2maps/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── scraper.py          # Web scrapers for RouteYou and Wikiloc
│   ├── gpx_parser.py       # GPX file parser
│   └── maps_converter.py   # Google Maps converter
├── requirements.txt
├── setup.py
└── README.md
```

## Dependencies

- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing
- `gpxpy` - GPX file parsing
- `googlemaps` - Google Maps API client
- `lxml` - XML parsing

## License

MIT License - see LICENSE file for details.

## Notes

This tool is designed for quick route discovery in the Malmedy area. The scrapers currently provide sample routes for demonstration. For production use, implement full web scraping with proper error handling and rate limiting.
