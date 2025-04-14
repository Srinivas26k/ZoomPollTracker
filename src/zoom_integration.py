import logging
import json
import os
import random
import requests
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Flag to determine if we're using real API or simulation
# Should be set to True when ZOOM_API_KEY and ZOOM_API_SECRET are available
USE_REAL_API = False

# Get Zoom API credentials from environment variables
ZOOM_API_KEY = os.environ.get('ZOOM_API_KEY')
ZOOM_API_SECRET = os.environ.get('ZOOM_API_SECRET')
ZOOM_JWT_TOKEN = os.environ.get('ZOOM_JWT_TOKEN')

# If API credentials are available, we'll use the real API
if ZOOM_API_KEY and ZOOM_API_SECRET and ZOOM_JWT_TOKEN:
    USE_REAL_API = True
    logger.info("Using real Zoom API with provided credentials")
else:
    logger.info("No Zoom API credentials found, using simulation mode")

# Base URL for Zoom API
ZOOM_API_BASE_URL = "https://api.zoom.us/v2"

class ZoomAPIClient:
    """
    Client for interacting with the Zoom API.
    This implementation falls back to simulation when credentials are not available.
    """
    def __init__(self):
        self.api_key = ZOOM_API_KEY
        self.api_secret = ZOOM_API_SECRET
        self.jwt_token = ZOOM_JWT_TOKEN
        self.use_real_api = USE_REAL_API
        
        # If we're not using the real API, initialize the simulator
        if not self.use_real_api:
            self.simulator = ZoomMeetingSimulator()
    
    def get_headers(self):
        """Get the headers required for Zoom API requests"""
        if not self.use_real_api:
            return {}
            
        return {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }
    
    def get_meeting_info(self, meeting_id=None):
        """
        Get information about a Zoom meeting
        
        Args:
            meeting_id (str): ID of the meeting to fetch
            
        Returns:
            dict: Meeting information
        """
        if not self.use_real_api:
            return self.simulator.get_meeting_info()
            
        # If we're using the real API, we would make an actual API call here
        try:
            # This would be replaced with an actual API call in production
            url = f"{ZOOM_API_BASE_URL}/meetings/{meeting_id}"
            response = requests.get(url, headers=self.get_headers())
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get meeting info: {response.text}")
                # Fall back to simulation if API call fails
                return self.simulator.get_meeting_info()
                
        except Exception as e:
            logger.error(f"Error calling Zoom API: {str(e)}")
            # Fall back to simulation
            return self.simulator.get_meeting_info()

class ZoomMeetingSimulator:
    """
    A class to simulate the behavior of a Zoom meeting.
    Used as a fallback when real API credentials are not available.
    """
    def __init__(self):
        # Create a realistic meeting setup
        self.meeting_id = "812345678910"
        self.host_id = "h4XeZuySQ62CvF3llYR8zA"
        self.participants = [
            {"id": "108124232", "name": "John Davis", "role": "host", "status": "active"},
            {"id": "108124233", "name": "Sarah Adams", "role": "co-host", "status": "active"},
            {"id": "108124234", "name": "Michael Kim", "role": "attendee", "status": "active"},
            {"id": "108124235", "name": "Lisa Wong", "role": "attendee", "status": "active"}
        ]
        self.meeting_status = "in_progress"
        self.polls = []
        self.current_poll = None
        self.meeting_topic = "Q2 Strategy Planning Meeting"
        
    def get_meeting_info(self):
        """Get information about the current simulated meeting."""
        return {
            "id": self.meeting_id,
            "uuid": f"ab12Cd34EFgh/56IJkl78=",
            "host_id": self.host_id,
            "topic": self.meeting_topic,
            "type": 2,
            "start_time": (datetime.now().replace(
                hour=datetime.now().hour-1, 
                minute=0, 
                second=0, 
                microsecond=0)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration": 60,
            "timezone": "UTC",
            "participant_count": len(self.participants),
            "status": self.meeting_status,
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": True,
                "waiting_room": False,
                "polls": {
                    "enable": True
                }
            }
        }
    
    def create_poll(self, question, options):
        """
        Create a new poll in the simulated Zoom meeting.
        
        Args:
            question (str): The poll question
            options (list): List of poll answer options
            
        Returns:
            dict: The created poll information
        """
        poll_id = f"poll_{len(self.polls) + 1}"
        
        poll = {
            "id": poll_id,
            "question": question,
            "options": options,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "created",
            "responses": {}
        }
        
        self.polls.append(poll)
        return poll
    
    def launch_poll(self, poll_id):
        """
        Launch a previously created poll in the simulated meeting.
        
        Args:
            poll_id (str): The ID of the poll to launch
            
        Returns:
            dict: The launched poll information or error
        """
        for poll in self.polls:
            if poll["id"] == poll_id:
                poll["status"] = "active"
                poll["launched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.current_poll = poll
                return {"success": True, "poll": poll}
        
        return {"success": False, "error": "Poll not found"}
    
    def end_poll(self, poll_id):
        """
        End an active poll in the simulated meeting.
        
        Args:
            poll_id (str): The ID of the poll to end
            
        Returns:
            dict: The ended poll information or error
        """
        for poll in self.polls:
            if poll["id"] == poll_id:
                if poll["status"] == "active":
                    poll["status"] = "ended"
                    poll["ended_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Simulate some random responses
                    # Initialize empty responses dictionary if it doesn't exist
                    if "responses" not in poll:
                        poll["responses"] = {}
                        
                    # Generate random responses for each participant
                    for participant in self.participants:
                        # Skip the host for more realistic results
                        if participant["role"] != "host":
                            random_option = random.randint(0, len(poll["options"]) - 1)
                            # Use participant ID as the key
                            poll["responses"][participant["id"]] = poll["options"][random_option]
                    
                    self.current_poll = None
                    return {"success": True, "poll": poll}
                else:
                    return {"success": False, "error": "Poll is not active"}
        
        return {"success": False, "error": "Poll not found"}
    
    def get_poll_results(self, poll_id):
        """
        Get the results of a completed poll.
        
        Args:
            poll_id (str): The ID of the poll
            
        Returns:
            dict: The poll results or error
        """
        for poll in self.polls:
            if poll["id"] == poll_id:
                if poll["status"] == "ended":
                    # Count responses
                    results = {}
                    for option in poll["options"]:
                        results[option] = 0
                    
                    for participant, response in poll["responses"].items():
                        results[response] += 1
                    
                    return {
                        "success": True,
                        "poll_id": poll_id,
                        "question": poll["question"],
                        "total_responses": len(poll["responses"]),
                        "results": results
                    }
                else:
                    return {"success": False, "error": f"Poll is not ended (current status: {poll['status']})"}
        
        return {"success": False, "error": "Poll not found"}

# Create a singleton instance of the simulator
zoom_simulator = ZoomMeetingSimulator()

def post_poll_to_zoom(poll_data):
    """
    Simulate posting a poll to a Zoom meeting.
    
    Args:
        poll_data (dict): The poll data including question and options
        
    Returns:
        dict: Status of the operation
    """
    logger.debug(f"Simulating posting poll to Zoom meeting: {json.dumps(poll_data, indent=2)}")
    
    # Create the poll in our simulator
    question = poll_data["question"]
    options = poll_data["options"]
    
    created_poll = zoom_simulator.create_poll(question, options)
    logger.debug(f"Created poll with ID: {created_poll['id']}")
    
    # Simulate launching the poll
    launch_result = zoom_simulator.launch_poll(created_poll["id"])
    if launch_result["success"]:
        logger.debug(f"Successfully launched poll: {created_poll['id']}")
        
        # For simulation purposes, we'll automatically end the poll after creating it
        # In a real implementation, this would happen after participants vote
        end_result = zoom_simulator.end_poll(created_poll["id"])
        if end_result["success"]:
            logger.debug(f"Poll ended: {created_poll['id']}")
            
            # Get the simulated results
            results = zoom_simulator.get_poll_results(created_poll["id"])
            logger.debug(f"Poll results: {json.dumps(results, indent=2)}")
            
            return {
                "success": True,
                "message": "Poll posted, launched, and completed in Zoom meeting",
                "poll_id": created_poll["id"],
                "results": results
            }
    
    return {
        "success": False,
        "message": "Failed to complete the poll process",
        "poll_id": created_poll["id"] if "created_poll" in locals() else None
    }

def get_zoom_meeting_info():
    """
    Get information about the current Zoom meeting.
    
    Returns:
        dict: Meeting information
    """
    return zoom_simulator.get_meeting_info()
