# Real-Time Zoom Poll Automation

A Python Flask application that automatically generates polls for Zoom meetings using transcript analysis, with all data stored temporarily in the browser.

![Zoom Poll Automation](static/img/screenshot.png)

## Overview

This application helps meeting hosts engage participants by automatically generating contextually relevant polls based on meeting content. The system uses AI to analyze meeting transcripts and create polls that reflect the current discussion topics.

### Key Features

- **Real-time poll generation** based on meeting transcript analysis
- **Automatic** or **manual** poll creation options
- **Temporary storage** using browser localStorage (no persistent data)
- **Zero-cost operation** with simulation mode for testing
- **Real-time updates** via WebSockets
- **Session history** for tracking all polls during a meeting
- **Data export** functionality for post-meeting analysis

## Technology Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Storage**: Browser localStorage (temporary)
- **Real-time Communication**: WebSockets (Socket.IO)
- **AI**: OpenAI integration (optional, can use built-in simulation)

## How It Works

1. **Transcript Analysis**: The system captures meeting transcript data in 10-minute segments
2. **Topic Detection**: AI analyzes the transcript to determine the current meeting topic
3. **Poll Generation**: Based on the topic, a relevant poll question with answer options is created
4. **Real-time Delivery**: The poll is immediately delivered to all connected clients
5. **Results Collection**: Responses are collected and displayed in real-time
6. **Temporary Storage**: All data is stored in browser localStorage for the duration of the session

## Getting Started

See the [User Guide](docs/USER_GUIDE.md) for detailed setup and usage instructions.

### Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Access the application at `http://localhost:5000`

## Documentation

- [User Guide](docs/USER_GUIDE.md) - Setup and usage instructions
- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md) - System architecture and extension points

## Simulation Mode

The application includes a simulation mode that works without actual Zoom API credentials. This is useful for:

- Testing the system before connecting to real meetings
- Demonstrating functionality to stakeholders
- Development and debugging

## Data Privacy

This application respects user privacy by:

- Storing all data in the browser's localStorage only
- Never sending meeting content to external servers
- Clearing all data when the browser is closed
- Providing manual export options to save needed data

## Real Zoom Integration

For real Zoom integration, you'll need:

1. A Zoom account with API capabilities
2. Zoom API credentials (API Key, Secret, JWT Token)
3. Update the `.env` file with your credentials
4. Set `has_zoom_credentials = True` in your environment

## License

[MIT License](LICENSE)

## Acknowledgements

- [Zoom API](https://marketplace.zoom.us/docs/api-reference/introduction/)
- [Flask](https://flask.palletsprojects.com/)
- [Socket.IO](https://socket.io/)
- [Bootstrap](https://getbootstrap.com/)
- [OpenAI](https://openai.com/) (optional integration)