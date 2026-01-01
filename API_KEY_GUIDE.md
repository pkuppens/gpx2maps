# Google Maps API Key Setup Guide

This guide explains how to obtain and safely use a Google Maps API key for the gpx2maps tool.

## Getting Your Google Maps API Key

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top of the page
4. Click "New Project"
5. Enter a project name (e.g., "gpx2maps")
6. Click "Create"

### Step 2: Enable Required APIs

1. In the Google Cloud Console, navigate to "APIs & Services" > "Library"
2. Search for and enable the following APIs:
   - **Maps JavaScript API**
   - **Directions API** (optional, for enhanced features)
   - **Static Maps API** (optional, for map images)

### Step 3: Create API Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Your new API key will be displayed
4. **Important**: Click "Restrict Key" to add security restrictions

### Step 4: Restrict Your API Key (Recommended)

For security, restrict your API key:

1. **Application restrictions**: Choose "None" for command-line tools
2. **API restrictions**: Select "Restrict key" and choose only the APIs you need:
   - Maps JavaScript API
   - Directions API
   - Static Maps API

3. Click "Save"

## Using Your API Key Safely

### Method 1: Environment Variable (Recommended)

The safest way to use your API key is through an environment variable.

#### On Linux/macOS:

```bash
# Add to ~/.bashrc or ~/.zshrc for persistence
export GOOGLE_MAPS_API_KEY="your-api-key-here"

# Or set for current session only
export GOOGLE_MAPS_API_KEY="your-api-key-here"
```

#### On Windows (PowerShell):

```powershell
# For current session
$env:GOOGLE_MAPS_API_KEY="your-api-key-here"

# For permanent (add to your PowerShell profile)
[System.Environment]::SetEnvironmentVariable('GOOGLE_MAPS_API_KEY', 'your-api-key-here', 'User')
```

#### On Windows (Command Prompt):

```cmd
# For current session
set GOOGLE_MAPS_API_KEY=your-api-key-here

# For permanent
setx GOOGLE_MAPS_API_KEY "your-api-key-here"
```

### Method 2: .env File (Alternative)

You can create a `.env` file in your project directory:

```bash
# .env file
GOOGLE_MAPS_API_KEY=your-api-key-here
```

**Important**: Add `.env` to your `.gitignore` file to prevent committing it to version control!

The `.gitignore` file already includes `.env`, so you're protected.

### Method 3: Command-Line Argument (Least Secure)

While supported, this method is **not recommended** because:
- API keys are visible in shell history
- API keys are visible in process lists
- API keys may be logged

```bash
gpx2maps convert route.gpx --api-key YOUR_API_KEY
```

## Using the API Key with gpx2maps

Once your API key is set as an environment variable, you can use gpx2maps without specifying it:

```bash
# Convert GPX to Google Maps
gpx2maps convert route.gpx

# The tool automatically reads from GOOGLE_MAPS_API_KEY environment variable
```

## API Key Security Best Practices

1. **Never commit API keys to version control**
   - The `.gitignore` file already includes `.env` and `config.ini`

2. **Restrict your API key** in Google Cloud Console
   - Limit which APIs can be called
   - Set usage quotas if needed

3. **Monitor API usage** in Google Cloud Console
   - Check for unexpected usage
   - Set up billing alerts

4. **Rotate keys regularly**
   - Generate new keys periodically
   - Delete old unused keys

5. **Use environment variables**
   - Don't hardcode keys in scripts
   - Don't pass keys as command-line arguments in production

## Pricing and Quotas

Google Maps Platform provides a **$200 monthly credit** that is **shared across all Google Maps APIs**:

- This $200 credit applies to your total usage across Maps JavaScript API, Directions API, Static Maps API, and other Google Maps Platform services
- Most personal and small-project use cases stay well within the free tier
- Monitor your usage in the Google Cloud Console to track spending
- Set up billing alerts to be notified before reaching the free tier limit

For detailed pricing information, visit the [Google Maps Platform Pricing](https://mapsplatform.google.com/pricing/) page.

## Troubleshooting

### "API key required" error

Make sure your environment variable is set:

```bash
# Check if variable is set (Linux/macOS)
echo $GOOGLE_MAPS_API_KEY

# Check if variable is set (Windows PowerShell)
echo $env:GOOGLE_MAPS_API_KEY
```

### "Invalid API key" error

- Check that you've enabled the required APIs in Google Cloud Console
- Verify there are no extra spaces in your API key
- Make sure the key isn't restricted in a way that prevents its use

### API key not found after setting environment variable

- Restart your terminal/shell
- Check that you're in the correct shell session
- For permanent settings, add to your shell configuration file

## Additional Resources

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [API Key Best Practices](https://developers.google.com/maps/api-key-best-practices)
- [Google Cloud Console](https://console.cloud.google.com/)
