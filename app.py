import os
import logging
from datetime import datetime, timedelta
from threading import Thread
import time
import json

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from flask_socketio import SocketIO

# Import our custom modules
from src.transcript_simulator import generate_transcript
from src.poll_generator import generate_poll_from_transcript
from src.zoom_integration import post_poll_to_zoom, get_zoom_meeting_info, ZoomAPIClient

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize SocketIO with the app
socketio = SocketIO(app)

# Initialize the Zoom API client
zoom_client = ZoomAPIClient()

# Check if we have Zoom API credentials
has_zoom_credentials = zoom_client.use_real_api

# Global variables to store the current poll and transcript
current_poll = None
current_transcript = None
last_poll_time = None
poll_interval = 15 * 60  # Default 15 minutes in seconds
connected_meeting = None

# Utility functions for the application
def get_recent_meetings():
    """Get a list of recent meetings (simulated)."""
    # In a real implementation, we would fetch this from the Zoom API
    # For demonstration purposes, we'll return some simulated meetings
    return [
        {
            "id": "812345678910",
            "topic": "Q2 Strategy Planning Meeting",
            "status": "in_progress",
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "participants_count": 4
        },
        {
            "id": "912345678911",
            "topic": "Product Development Roadmap",
            "status": "scheduled",
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "participants_count": 0
        },
        {
            "id": "812345678912",
            "topic": "Team Onboarding Session",
            "status": "in_progress",
            "start_time": (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "participants_count": 6
        }
    ]

def get_default_meeting():
    """Get a default meeting object for simulation."""
    # Get the meeting info from our simulator
    meeting_info = get_zoom_meeting_info()
    
    # Format it for our UI
    return {
        "id": meeting_info["id"],
        "topic": meeting_info["topic"],
        "status": meeting_info["status"],
        "start_time": meeting_info["start_time"],
        "host": {
            "name": "John Davis",
            "id": "user123"
        },
        "participants_count": meeting_info["participant_count"] if "participant_count" in meeting_info else 4
    }

@app.route('/')
def index():
    """Render the main page or redirect to connection page if not connected."""
    # If we're not connected to a meeting yet, redirect to the connect page
    if connected_meeting is None and not session.get('simulation_mode', False):
        return redirect(url_for('connect'))
        
    return main_page()

@app.route('/app')
def main_page():
    """Render the main application page with polls."""
    global current_poll, current_transcript, last_poll_time, poll_interval
    
    # Set a shorter interval for demo purposes if specified
    demo_interval = request.args.get('interval', None)
    if demo_interval and demo_interval.isdigit():
        poll_interval = int(demo_interval)
        
    # Initialize with data if none exists yet
    if current_poll is None:
        # Generate initial data
        current_transcript = generate_transcript()
        current_poll = generate_poll_from_transcript(current_transcript)
        last_poll_time = datetime.now()
    
    # Calculate time until next poll
    time_until_next_poll = None
    if last_poll_time:
        next_poll_time = last_poll_time + timedelta(seconds=poll_interval)
        time_until_next_poll = (next_poll_time - datetime.now()).total_seconds()
        if time_until_next_poll < 0:
            time_until_next_poll = 0
    
    return render_template('index.html', 
                           poll=current_poll, 
                           transcript=current_transcript,
                           last_poll_time=last_poll_time,
                           time_until_next=time_until_next_poll,
                           poll_interval=poll_interval,
                           meeting=connected_meeting or get_default_meeting(),
                           simulation_mode=session.get('simulation_mode', False))

@app.route('/connect')
def connect():
    """Render the connection page to link with a Zoom meeting."""
    # Get list of recent meetings (simulated in this case)
    recent_meetings = get_recent_meetings()
    
    return render_template('connect.html', 
                           recent_meetings=recent_meetings,
                           has_credentials=has_zoom_credentials)

@app.route('/connect/meeting', methods=['POST'])
def connect_to_meeting():
    """Connect to a specific Zoom meeting."""
    global connected_meeting, poll_interval
    
    # Get meeting details from form
    meeting_id = request.form.get('meeting_id')
    meeting_passcode = request.form.get('meeting_passcode')
    poll_interval_input = request.form.get('poll_interval')
    
    if poll_interval_input and poll_interval_input.isdigit():
        poll_interval = int(poll_interval_input)
    
    # If we don't have API credentials, redirect to simulation
    if not has_zoom_credentials:
        return redirect(url_for('simulate_meeting'))
        
    # In a real implementation, we would connect to the Zoom meeting API here
    # For now, we'll just simulate a successful connection
    connected_meeting = {
        "id": meeting_id,
        "topic": "Q2 Strategy Planning Meeting",
        "status": "in_progress",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "host": {
            "name": "John Davis",
            "id": "user123"
        },
        "participants_count": 4
    }
    
    flash('Successfully connected to Zoom meeting', 'success')
    return redirect(url_for('main_page'))

@app.route('/simulate', methods=['POST'])
def simulate_meeting():
    """Activate simulation mode when no real Zoom credentials exist."""
    # Set simulation mode flag in session
    session['simulation_mode'] = True
    
    # Get default simulated meeting
    global connected_meeting
    connected_meeting = get_default_meeting()
    
    flash('Simulation mode activated', 'info')
    return redirect(url_for('main_page'))

@app.route('/api/update-interval', methods=['POST'])
def update_interval():
    """Update the poll generation interval."""
    global poll_interval
    
    data = request.get_json()
    if data and 'interval' in data:
        try:
            new_interval = int(data['interval'])
            if new_interval < 1:
                return jsonify({'success': False, 'message': 'Interval must be at least 1 second'}), 400
                
            poll_interval = new_interval
            return jsonify({'success': True, 'message': f'Interval updated to {poll_interval} seconds'})
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid interval value'}), 400
    
    return jsonify({'success': False, 'message': 'No interval provided'}), 400

@app.route('/api/generate-poll', methods=['POST'])
def api_generate_poll():
    """Generate a new poll on demand."""
    global current_poll, current_transcript, last_poll_time
    
    # Generate new data
    current_transcript = generate_transcript()
    current_poll = generate_poll_from_transcript(current_transcript)
    last_poll_time = datetime.now()
    
    # Emit the new poll to all connected clients
    socketio.emit('poll_update', {
        'poll': current_poll,
        'transcript': current_transcript,
        'timestamp': last_poll_time.strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Simulate posting to Zoom
    post_poll_to_zoom(current_poll)
    
    return jsonify({
        'success': True, 
        'poll': current_poll, 
        'transcript': current_transcript,
        'timestamp': last_poll_time.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/get-poll')
def get_poll():
    """Get the current poll data."""
    global current_poll, current_transcript, last_poll_time
    
    if current_poll is None:
        return jsonify({'success': False, 'message': 'No poll has been generated yet'}), 404
    
    time_until_next_poll = None
    if last_poll_time:
        next_poll_time = last_poll_time + timedelta(seconds=poll_interval)
        time_until_next_poll = (next_poll_time - datetime.now()).total_seconds()
        if time_until_next_poll < 0:
            time_until_next_poll = 0
    
    return jsonify({
        'success': True,
        'poll': current_poll,
        'transcript': current_transcript,
        'timestamp': last_poll_time.strftime('%Y-%m-%d %H:%M:%S') if last_poll_time else None,
        'timeUntilNext': time_until_next_poll
    })

# Background task to generate polls at regular intervals
def poll_generation_task():
    global current_poll, current_transcript, last_poll_time
    
    while True:
        now = datetime.now()
        
        # Check if it's time to generate a new poll
        if last_poll_time is None or (now - last_poll_time).total_seconds() >= poll_interval:
            logger.debug("Generating new poll...")
            
            # Generate new transcript and poll
            current_transcript = generate_transcript()
            current_poll = generate_poll_from_transcript(current_transcript)
            last_poll_time = now
            
            # Emit the new poll to all connected clients
            socketio.emit('poll_update', {
                'poll': current_poll,
                'transcript': current_transcript,
                'timestamp': last_poll_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # Simulate posting to Zoom
            post_poll_to_zoom(current_poll)
            
            logger.debug(f"New poll generated: {current_poll}")
        
        # Sleep for 1 second before next check
        time.sleep(1)

# Start the background task when the app starts
background_thread = None

@socketio.on('connect')
def handle_connect():
    global background_thread
    if background_thread is None:
        background_thread = Thread(target=poll_generation_task)
        background_thread.daemon = True
        background_thread.start()



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
