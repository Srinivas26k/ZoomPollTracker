# Real-Time Zoom Poll Automation - User Guide

## Introduction

The Real-Time Zoom Poll Automation system automatically generates and presents polls during live Zoom meetings. By analyzing meeting transcripts, the application creates contextually relevant polls to engage participants without disrupting meeting flow. All data is stored temporarily in browser local storage for the duration of the session, ensuring privacy and minimizing resource usage.

## System Features

- **Automatic Poll Generation**: Creates polls based on real-time meeting transcript content
- **Temporary Storage**: Uses browser's localStorage for session-only data persistence
- **Real-time Updates**: Pushes new polls to all connected clients instantly
- **Meeting Simulation**: Works in simulation mode with no API credentials
- **Poll History**: Maintains a session history of previous polls with easy recall
- **Analytics**: Provides basic analytics on poll topics and frequency
- **Data Export**: Export session data for offline analysis

## Setup Guide for Windows

### Prerequisites

- Python 3.10 or newer
- Git (optional, for cloning the repository)
- Web browser (Chrome, Firefox, or Edge recommended)
- Zoom account (optional, for real API integration)

### Installation Steps

1. **Clone or Download the Repository**

   ```
   git clone https://github.com/yourusername/zoom-poll-automation.git
   ```
   
   Or download and extract the ZIP file from the repository.

2. **Set Up a Python Virtual Environment**

   Open Command Prompt and navigate to the project directory:
   
   ```
   cd path\to\zoom-poll-automation
   ```
   
   Create a virtual environment:
   
   ```
   python -m venv venv
   ```
   
   Activate the virtual environment:
   
   ```
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Environment Variables (Optional)**

   For real Zoom integration, create a `.env` file in the project root with your Zoom API credentials:
   
   ```
   ZOOM_API_KEY=your_zoom_api_key
   ZOOM_API_SECRET=your_zoom_api_secret
   ZOOM_JWT_TOKEN=your_zoom_jwt_token
   ```
   
   For using OpenAI's API instead of the default AI:
   
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application

1. **Start the Flask Server**

   From the project directory with the virtual environment activated:
   
   ```
   python main.py
   ```
   
   Or:
   
   ```
   flask run
   ```

2. **Access the Application**

   Open your web browser and navigate to:
   
   ```
   http://localhost:5000
   ```

3. **Connect to a Meeting**

   - Click "Connect to Meeting" on the homepage
   - Enter a meeting ID (can be simulated if no API credentials)
   - Set your preferred poll generation interval
   - Click "Connect" or "Simulate Meeting"

4. **Using the Application During a Meeting**

   - Monitor the automated poll generation
   - Use manual controls to generate polls on demand
   - View and interact with poll history
   - Export meeting data as needed

## Usage Guide

### Main Dashboard

The main dashboard displays:

- **Control Panel**: Set poll intervals, generate polls manually, view system status
- **Zoom Meeting Interface**: Simulated/real meeting with participants and controls
- **Active Poll**: Currently active poll with options
- **Meeting Transcript**: Last 10 minutes of meeting transcript
- **Poll History**: Recent polls from the current session
- **Analytics**: Topic distribution for generated polls

### Poll Generation

Polls are generated in two ways:

1. **Automatic Generation**: 
   - Polls are created at regular intervals (default: 15 minutes)
   - Based on the last 10 minutes of meeting transcript
   - Topics are determined by AI analysis

2. **Manual Generation**:
   - Click "Generate Poll Now" button
   - Creates a poll immediately using the current transcript
   - Resets the automatic generation timer

### Real-time Features

- **Live Updates**: All connected clients see new polls immediately
- **Session History**: Previous polls are stored in browser local storage
   - Click any poll in the history to reload it
   - History is cleared when the browser is closed
- **Analytics**: View topic distribution of polls in the current session
- **Data Export**: Export all session data as JSON for further analysis

### Simulation vs Real Mode

- **Simulation Mode**: Works without Zoom API credentials
   - Uses simulated meeting transcripts
   - Demonstrates full functionality for evaluation
- **Real Mode**: Requires Zoom API credentials
   - Connects to actual Zoom meetings
   - Uses real meeting transcripts for poll generation

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Make sure all dependencies are installed
   - Check for Python 3.10+ installation
   - Ensure ports 5000 is available

2. **No polls are generated**
   - Check browser console for errors
   - Verify WebSocket connection is established
   - Ensure JavaScript is enabled in your browser

3. **Simulation mode not working**
   - Clear browser cache and cookies
   - Try a different browser
   - Restart the Flask server

## Best Practices

- **Optimal Poll Frequency**: Set poll interval to 15-20 minutes for best results
- **Meeting Size**: Works best with 5-25 participant meetings
- **Poll Topics**: The AI works best with technical, business, or educational meetings
- **Data Management**: Export poll data before ending the session to preserve results

## Privacy and Data Handling

- All meeting data is processed locally
- Transcript data and polls are stored only in the browser's localStorage
- Data is cleared when the browser is closed or manually cleared
- No permanent storage of meeting content on server side
- Export functionality allows saving data if needed

---

© 2025 Real-Time Zoom Poll Automation