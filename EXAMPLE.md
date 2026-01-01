# Quick Start Example

This example shows a complete workflow from searching routes to getting a Google Maps link.

## Step 1: Search for Routes

```bash
gpx2maps search --location Malmedy --distance 10
```

Output:
```
🔍 Searching for routes near Malmedy within 10.0km...
   Filtering for routes with prefix: MDY

📡 Searching RouteYou...
   Found 2 routes on RouteYou

📡 Searching Wikiloc...
   Found 3 routes on Wikiloc

✅ Found 5 total routes:

1. MDY-01: Malmedy City Walk
   Distance: 5.2 km
   URL: https://www.routeyou.com/en-be/route/view/malmedy-city-walk
...
```

## Step 2: Download a Route

Choose a route from the search results and download it:

```bash
gpx2maps download --url "https://www.routeyou.com/en-be/route/view/malmedy-city-walk"
```

Output:
```
⬇️  Downloading route from https://www.routeyou.com/en-be/route/view/malmedy-city-walk...
✅ Downloaded to: gpx_files/routeyou_malmedy-city-walk.gpx
```

## Step 3: Convert to Google Maps

Convert the downloaded GPX file to a Google Maps link:

```bash
export GOOGLE_MAPS_API_KEY="your-api-key-here"
gpx2maps convert gpx_files/routeyou_malmedy-city-walk.gpx
```

Output:
```
📂 Parsing GPX file: gpx_files/routeyou_malmedy-city-walk.gpx...
   Route: RouteYou Route
   Points: 8
   Distance: 1.59 km

🗺️  Converting to Google Maps...

✅ Google Maps link:
   https://www.google.com/maps/dir/50.4233,6.0294/50.425,6.031/.../50.4233,6.0294/@50.4233,6.0294,12z/data=!4m2!4m1!3e2
```

## Step 4: Save the Link

Save the link to a file for easy access:

```bash
gpx2maps convert gpx_files/routeyou_malmedy-city-walk.gpx --output walk-today.txt
```

Now you can open `walk-today.txt` and click the link to see the route in Google Maps!

## Step 5: List All Routes

See all your downloaded routes:

```bash
gpx2maps list
```

Output:
```
📁 GPX files in 'gpx_files':

• routeyou_malmedy-city-walk.gpx
  Name: RouteYou Route
  Distance: 1.59 km
  Points: 8
```

## Additional Tips

### Filter by Distance

Only show routes shorter than 8km:
```bash
gpx2maps search --distance 8
```

### Search Specific Source

Search only RouteYou or Wikiloc:
```bash
gpx2maps search --source routeyou
gpx2maps search --source wikiloc
```

### Filter by Prefix

Filter routes by a specific prefix:
```bash
gpx2maps search --prefix MDY
```

## Note

The sample implementation provides example routes for the Malmedy area. For production use with real web scraping, you would need to implement the actual HTTP requests and HTML parsing logic in the scraper modules.
