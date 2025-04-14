# Real-Time Zoom Poll Automation - Technical Documentation

## System Architecture

The Zoom Poll Automation system follows a client-server architecture with:

1. **Backend (Flask)**: Python Flask application providing API endpoints and WebSocket communication
2. **Frontend (JavaScript/HTML/CSS)**: Browser-based UI with real-time updates via WebSockets
3. **Storage**: Client-side only, using browser's localStorage
4. **External Services** (optional): Zoom API, OpenAI API

## Component Overview

### Server-Side Components

#### Main Application (`app.py`)
- Initializes Flask server and Socket.IO
- Defines routes and API endpoints
- Manages WebSocket connections
- Coordinates poll generation in the background

#### Transcript Simulation (`src/transcript_simulator.py`)
- Generates realistic meeting transcript snippets
- Creates topic-focused content for testing
- Simulates real-time transcript segments

#### Poll Generator (`src/poll_generator.py`)
- Analyzes transcript content to determine topics
- Creates contextually relevant polls
- Generates answer options based on topic

#### Zoom Integration (`src/zoom_integration.py`)
- Handles communication with Zoom API
- Provides fallback simulation when no credentials exist
- Posts polls to meetings and retrieves results

### Client-Side Components

#### Application Logic (`static/js/app.js`)
- Manages UI updates and user interactions
- Handles WebSocket communication with server
- Coordinates real-time updates

#### Local Storage (`static/js/storage.js`)
- Manages temporary data persistence
- Stores meeting information, polls, and user settings
- Provides history and analytics functionality

#### Styling (`static/css/style.css`)
- Custom styling for application components
- Responsive design for various screen sizes
- Animation and visual feedback

## Data Flow

1. **Poll Generation Process**:
   - Transcript is generated/captured from Zoom meeting
   - AI analysis determines meeting topic and content
   - Poll is created with relevant question and options
   - Poll is broadcast to all connected clients via WebSocket
   - Poll data is stored in localStorage for history

2. **Real-time Communication**:
   - Server emits `poll_update` events via Socket.IO
   - Clients listen for events and update UI
   - Manual actions by users trigger API calls to server
   - Server responds with updated data

## API Endpoints

### `/api/generate-poll` (POST)
- Generates a new poll on demand
- Returns poll data, transcript, and timestamp

### `/api/get-poll` (GET)
- Retrieves the current active poll
- Returns poll data, transcript, and timing information

### `/api/update-interval` (POST)
- Updates the automatic poll generation interval
- Accepts interval in seconds

### `/connect/meeting` (POST)
- Connects to a specified Zoom meeting
- Accepts meeting ID, passcode, and poll interval

## WebSocket Events

### `poll_update`
- Emitted when a new poll is generated
- Contains poll data, transcript, and timestamp

### `connect`
- Client connection event
- Triggers background polling task if not running

## Local Storage Structure

### `zoom_poll_automation_meeting`
- Current meeting information
- Contains meeting ID, topic, status, etc.

### `zoom_poll_automation_polls`
- Array of poll objects from the current session
- Contains questions, options, timestamps, and topics

### `zoom_poll_automation_settings`
- User preferences
- Includes poll interval, notification settings, etc.

### `zoom_poll_automation_stats`
- Analytics data for the current session
- Tracks topic distributions and poll counts

## Extension Points

### Adding New AI Models

To use a different AI model for poll generation:

1. Create a new module in the `src` directory
2. Implement analysis functions similar to `analyze_transcript_topic`
3. Update `generate_poll_from_transcript` to use your new model
4. Update environment variables as needed

### Implementing Real Zoom Integration

To connect with the actual Zoom API:

1. Register a Zoom App in the Zoom Marketplace
2. Obtain API credentials (API key, Secret, JWT)
3. Update the `ZoomAPIClient` class in `zoom_integration.py`
4. Implement real API calls for each method

### Adding New Analytics Features

To extend the analytics capabilities:

1. Update the `updatePollStats` function in `storage.js`
2. Add new visualization logic in `showPollAnalytics`
3. Create additional UI components in `index.html`

## Dependencies

### Backend
- Flask: Web framework
- Flask-SocketIO: WebSocket support
- Python-dotenv: Environment variable management
- Requests: HTTP client for API calls
- OpenAI (optional): For advanced AI capabilities

### Frontend
- Socket.IO Client: Real-time communication
- Bootstrap: UI framework
- Font Awesome: Icons
- Browser localStorage API: Client-side storage

## Deployment Considerations

### Production Setup
- Use a production WSGI server (Gunicorn, uWSGI)
- Enable Flask's production mode
- Consider Redis for Socket.IO message queue (for scaling)
- Implement proper error handling and logging

### Security Considerations
- Store API keys securely (not in code)
- Use HTTPS for all communication
- Implement rate limiting for API endpoints
- Validate all user input
- Consider adding user authentication

## Performance Optimization

- Minimize WebSocket message size
- Implement pagination for poll history
- Use debouncing for user interactions
- Optimize localStorage usage (clean old data periodically)
- Consider IndexedDB for larger storage needs

---

© 2025 Real-Time Zoom Poll Automation