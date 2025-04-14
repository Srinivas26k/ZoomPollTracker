# Technical Documentation for Real-Time Zoom Poll Automation

This document provides detailed technical information about the project architecture, components, and integration points.

## System Architecture

The Real-Time Zoom Poll Automation project is built with a modular architecture consisting of the following components:

### 1. Core Application (app.py)
- Flask web application that serves as the central coordination point
- Manages the timing and scheduling of poll generation
- Handles WebSocket connections for real-time updates
- Exposes API endpoints for manual control

### 2. Transcript Simulator (src/transcript_simulator.py)
- Generates realistic meeting transcript data
- Simulates capturing the last 10 minutes of a meeting
- Creates topic-specific conversations with timestamps

### 3. Poll Generator (src/poll_generator.py)
- Analyzes transcript content to determine the meeting topic
- Generates contextually relevant poll questions based on the topic
- Provides appropriate answer options for the generated question
- Simulates the role of Ollama/Llama 3.2 in a production environment

### 4. Zoom Integration Simulator (src/zoom_integration.py)
- Simulates the Zoom SDK functionality
- Provides methods for creating, launching, and ending polls
- Simulates participant responses and poll results

### 5. Frontend Components
- HTML templates for UI rendering
- JavaScript for real-time updates and user interactions
- CSS for styling and animations

## Module Details

### Transcript Simulator

The transcript simulator creates realistic meeting conversation data with:

- Random selection of meeting topics
- Participant dialogue with timestamps
- Topic-specific phrases and terminology
- Natural conversation flow with questions and responses

Implementation details:
- Configurable meeting duration (default: 10 minutes)
- Varied participant count and messaging frequency
- Timestamped messages for chronological ordering

### Poll Generator

The poll generator analyzes transcripts and generates polls through:

1. **Topic Analysis:** Identifies the primary meeting topic based on keyword frequency
2. **Question Selection:** Chooses a relevant question template for the identified topic
3. **Option Generation:** Provides contextually appropriate answer options
4. **JSON Formatting:** Returns a structured poll object

The module simulates AI-powered poll generation by:
- Using predefined templates rather than actual AI processing
- Applying basic text analysis to match topics
- Ensuring generated polls are relevant to the meeting content

### Zoom Integration Simulator

This module simulates what would normally be handled by the Zoom SDK:

- **Meeting Management:** Tracks meeting status, participants, and polls
- **Poll Creation:** Interface for generating and storing polls
- **Poll Launching:** Simulates poll distribution to participants
- **Results Collection:** Generates simulated responses from participants

## Configuration and Customization

### Poll Generation Interval

The default interval for poll generation is 15 minutes (900 seconds). This can be customized through:

1. **Web Interface:** Using the control panel input field
2. **URL Parameter:** Adding `?interval=X` to the URL, where X is seconds
3. **Environment Variable:** Setting `POLL_INTERVAL` (not implemented yet, future enhancement)

### Transcript Topics

The system supports the following meeting topics:
- Project Status Update
- Marketing Strategy Discussion
- Product Development Roadmap
- Customer Feedback Review
- Team Building Activities
- Budget Planning for Next Quarter
- New Feature Implementation
- User Experience Improvements
- Sales Performance Review
- Technical Architecture Discussion

To extend with new topics:
1. Add the topic to `MEETING_TOPICS` list in `transcript_simulator.py`
2. Add corresponding phrases to `TOPIC_PHRASES` dictionary
3. Add appropriate poll templates to `POLL_TEMPLATES` in `poll_generator.py`

## Integration with Real Zoom SDK

To integrate with the actual Zoom SDK instead of simulation:

1. Register a Zoom App in the [Zoom Developer Portal](https://marketplace.zoom.us/)
2. Configure Meeting SDK credentials
3. Replace the simulation functions in `zoom_integration.py` with actual SDK calls:

```python
# Example of real Zoom SDK integration (pseudocode)
from zoom_sdk import ZoomMeetingSDK

zoom_client = ZoomMeetingSDK(api_key, api_secret)

def post_poll_to_zoom(poll_data):
    meeting_id = get_current_meeting_id()
    
    # Create the poll using actual Zoom API
    poll = zoom_client.create_poll(
        meeting_id=meeting_id,
        title="Meeting Poll",
        questions=[{
            "name": poll_data["question"],
            "type": "single",
            "answers": poll_data["options"]
        }]
    )
    
    # Launch the poll
    zoom_client.launch_poll(meeting_id, poll["id"])
    
    return {
        "success": True,
        "message": "Poll posted to Zoom meeting",
        "poll_id": poll["id"]
    }
