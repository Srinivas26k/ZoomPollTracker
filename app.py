import os
import logging
from datetime import datetime, timedelta
from threading import Thread
import time

from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO

# Import our custom modules
from src.transcript_simulator import generate_transcript
from src.poll_generator import generate_poll_from_transcript
from src.zoom_integration import post_poll_to_zoom

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize SocketIO with the app
socketio = SocketIO(app)

# Global variables to store the current poll and transcript
current_poll = None
current_transcript = None
last_poll_time = None
poll_interval = 15 * 60  # Default 15 minutes in seconds

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main page of the application."""
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
                           poll_interval=poll_interval)

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
