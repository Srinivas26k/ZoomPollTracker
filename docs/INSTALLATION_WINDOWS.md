# Installation Guide for Windows

This guide provides detailed instructions for installing and setting up the Real-Time Zoom Poll Automation application on a Windows machine.

## System Requirements

- Windows 10 or Windows 11 (64-bit)
- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for API access

## Step 1: Install Python

1. Download the latest Python installer from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Choose "Customize installation" and ensure pip is selected
5. Complete the installation

Verify Python is installed correctly by opening Command Prompt and typing:
```
python --version
pip --version
```

## Step 2: Download the Application

### Option 1: Download ZIP Archive
1. Download the latest release ZIP file from the project repository
2. Extract the ZIP file to a location on your computer (e.g., `C:\ZoomPollAutomation`)

### Option 2: Clone with Git
If you have Git installed, you can clone the repository:
```
git clone https://github.com/yourusername/zoom-poll-automation.git C:\ZoomPollAutomation
```

## Step 3: Create a Virtual Environment

Creating a virtual environment is recommended to avoid package conflicts:

1. Open Command Prompt as Administrator
2. Navigate to the application directory:
   ```
   cd C:\ZoomPollAutomation
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```

## Step 4: Install Dependencies

With the virtual environment activated, install the required packages:

```
pip install -r requirements.txt
```

This will install all necessary dependencies including Flask, Flask-SocketIO, requests, and others.

## Step 5: Set Up Environment Variables

Create a `.env` file in the application root directory with the following variables:

```
# Zoom API Credentials
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret

# OpenAI API Key (Optional - for OpenAI features)
OPENAI_API_KEY=your_openai_api_key

# Application Settings
SESSION_SECRET=your_random_secret_key
```

### Obtaining API Credentials

#### Zoom API Credentials
1. Go to the [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Sign in with your Zoom account
3. Click "Develop" > "Build App"
4. Select "Server-to-Server OAuth" app type
5. Follow the prompts to create your app
6. Once created, find your Client ID and Client Secret in the app credentials section

#### OpenAI API Key (Optional)
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create a new API key
4. Copy the key and add it to your `.env` file

## Step 6: Install Ollama (Optional)

To use the local AI model features, install Ollama:

1. Download Ollama from [ollama.ai](https://ollama.ai/download)
2. Run the installer and follow the instructions
3. Once installed, open Command Prompt and run:
   ```
   ollama pull llama3:3b
   ```
   This downloads the LLaMA 3.2 3B model for local processing

## Step 7: Start the Application

With everything set up, you can now start the application:

1. Ensure your virtual environment is activated
2. Run the application:
   ```
   python main.py
   ```
3. The application should start and be available at `http://localhost:5000`

## Step 8: Connect to Zoom

Once the application is running:

1. Open your browser and go to `http://localhost:5000`
2. Click "Connect to Zoom Meeting"
3. Enter a meeting ID to connect to an active Zoom meeting
4. The application will start generating polls based on the meeting content

## Troubleshooting

### Application Won't Start
- Ensure Python is installed and in your PATH
- Check that all dependencies are installed
- Verify the `.env` file exists with the required variables

### Can't Connect to Zoom
- Verify your Zoom API credentials are correct
- Ensure the Zoom meeting ID is valid
- Check that your app has the necessary Zoom API permissions

### Model Selection Not Working
- For local models: ensure Ollama is running (`ollama serve` command)
- For OpenAI: verify your API key is valid and has sufficient quota

### Audio Transcription Issues
- Check microphone settings and permissions
- If using OpenAI transcription, verify your API key and quota

## Running as a Service (Advanced)

To run the application as a Windows service:

1. Install NSSM (Non-Sucking Service Manager):
   - Download from [nssm.cc](https://nssm.cc/download)
   - Extract to a folder in your PATH

2. Create a batch file to start the application:
   ```batch
   @echo off
   cd C:\ZoomPollAutomation
   call venv\Scripts\activate
   python main.py
   ```
   Save as `start_zoom_poll_app.bat`

3. Install as a service using NSSM:
   ```
   nssm install ZoomPollAutomation
   ```
   - Path: `C:\ZoomPollAutomation\start_zoom_poll_app.bat`
   - Startup directory: `C:\ZoomPollAutomation`
   - Service name: ZoomPollAutomation

4. Start the service:
   ```
   nssm start ZoomPollAutomation
   ```

## Next Steps

After successful installation:

- Explore the different AI model options in the UI
- Configure the poll generation interval
- Check the API documentation for integration options

For more information, refer to the [User Guide](USER_GUIDE.md) and [API Documentation](API_DOCUMENTATION.md).

## Support

If you encounter issues not covered in this guide, please:
- Check the project wiki for known issues
- Submit a detailed bug report through the issue tracker
- Contact support at support@yourdomain.com