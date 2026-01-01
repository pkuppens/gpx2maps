# gpx2maps Quick Reference

## Installation
```bash
pip install -r requirements.txt
pip install -e .
```

## Common Commands

### Search for routes
```bash
gpx2maps search --location Malmedy --distance 10
```

### Download a route
```bash
gpx2maps download --url "https://www.routeyou.com/route/view/..."
```

### Convert to Google Maps
```bash
export GOOGLE_MAPS_API_KEY="your-api-key"
gpx2maps convert route.gpx
```

### List downloaded routes
```bash
gpx2maps list
```

## Command Options

### search
- `--location` - Location to search (default: Malmedy)
- `--distance` - Distance in km (default: 10)
- `--source` - Source website: routeyou, wikiloc, or all (default: all)
- `--prefix` - Route prefix filter (default: MDY)

### download
- `--url` - Route URL (required)
- `--output` - Output filename (optional)

### convert
- `gpx_file` - Path to GPX file (required)
- `--api-key` - Google Maps API key (optional, use env var instead)
- `--output` - Output file for the link (optional)

### list
- `--directory` - Directory containing GPX files (default: gpx_files)

## Examples

Search only RouteYou within 8km:
```bash
gpx2maps search --distance 8 --source routeyou
```

Download and convert in one go:
```bash
gpx2maps download --url "https://www.routeyou.com/route/view/12345"
gpx2maps convert gpx_files/routeyou_12345.gpx --output walk.txt
```

## Environment Variables
- `GOOGLE_MAPS_API_KEY` - Your Google Maps API key (recommended over --api-key flag)

## File Locations
- Downloaded GPX files: `./gpx_files/`
- Format: `routeyou_<route-id>.gpx` or `wikiloc_<route-id>.gpx`

## Support
For detailed documentation, see:
- README.md - Full documentation
- EXAMPLE.md - Step-by-step examples
- SUMMARY.md - Implementation details
