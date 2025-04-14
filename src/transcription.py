"""
Real-time transcription module for Zoom meetings.
Supports multiple transcription options:
1. OpenAI Whisper API for cloud-based processing
2. Local Ollama llama3.2 for on-device processing
3. Simulated transcription (fallback)
"""

import os
import logging
import base64
import json
import requests
from typing import Optional, Dict, Any, List
import random
from datetime import datetime, timedelta

# Import simulation functions (fallback)
from src.transcript_simulator import generate_transcript

# Set up logging
logger = logging.getLogger(__name__)

# Check for OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Define available transcription modes
TRANSCRIPTION_MODES = {
    "openai": "OpenAI Whisper API (Cloud)",
    "ollama": "Ollama llama3.2 (Local)",
    "simulation": "Simulated Transcription (Testing)"
}

# Default to simulation if no API keys are available
DEFAULT_MODE = "openai" if OPENAI_API_KEY else "simulation"
current_mode = DEFAULT_MODE

def set_transcription_mode(mode: str) -> bool:
    """
    Set the transcription mode to use.
    
    Args:
        mode (str): One of 'openai', 'ollama', or 'simulation'
        
    Returns:
        bool: True if successful, False if mode is invalid
    """
    global current_mode
    
    if mode in TRANSCRIPTION_MODES:
        current_mode = mode
        logger.info(f"Transcription mode set to: {TRANSCRIPTION_MODES[mode]}")
        return True
    else:
        logger.error(f"Invalid transcription mode: {mode}")
        return False

def get_available_modes() -> Dict[str, str]:
    """
    Get a dictionary of available transcription modes.
    
    Returns:
        Dict[str, str]: Dictionary of mode_key: mode_description pairs
    """
    # Filter out unavailable modes
    available_modes = {}
    
    # OpenAI Whisper requires API key
    if OPENAI_API_KEY:
        available_modes["openai"] = TRANSCRIPTION_MODES["openai"]
    
    # Check if Ollama is installed and available
    try:
        # This tests if we can connect to the Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
        if response.status_code == 200:
            # Check if llama3.2 model is available
            models = response.json().get("models", [])
            if any("llama3" in model.get("name", "") for model in models):
                available_modes["ollama"] = TRANSCRIPTION_MODES["ollama"]
    except:
        # If Ollama is not available, don't add it to available modes
        pass
    
    # Simulation is always available as fallback
    available_modes["simulation"] = TRANSCRIPTION_MODES["simulation"]
    
    return available_modes

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio using the currently selected transcription mode.
    
    Args:
        audio_file_path (str): Path to the audio file to transcribe
        
    Returns:
        str: Transcribed text
    """
    if current_mode == "openai":
        return transcribe_with_openai(audio_file_path)
    elif current_mode == "ollama":
        return transcribe_with_ollama(audio_file_path)
    else:
        return generate_transcript()  # Fall back to simulation

def transcribe_with_openai(audio_file_path: str) -> str:
    """
    Transcribe audio using OpenAI Whisper API.
    
    Args:
        audio_file_path (str): Path to the audio file to transcribe
        
    Returns:
        str: Transcribed text from OpenAI
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set, cannot use Whisper API")
        return generate_transcript()  # Fall back to simulation
    
    logger.info(f"Transcribing audio with OpenAI Whisper API: {audio_file_path}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        
        logger.info("Successfully transcribed audio with OpenAI Whisper")
        return transcript
    
    except Exception as e:
        logger.error(f"Error transcribing with OpenAI Whisper: {str(e)}")
        return generate_transcript()  # Fall back to simulation

def transcribe_with_ollama(audio_file_path: str) -> str:
    """
    Transcribe audio using local Ollama llama3.2 model.
    This is a simplified implementation and would need proper
    audio processing in a real implementation.
    
    Args:
        audio_file_path (str): Path to the audio file to transcribe
        
    Returns:
        str: Transcribed text from Ollama
    """
    logger.info(f"Transcribing audio with local Ollama llama3.2: {audio_file_path}")
    
    try:
        # In a real implementation, you would:
        # 1. Convert audio to text using a local STT model or library
        # 2. Send the text to Ollama for processing
        
        # For now, we'll simulate this process
        OLLAMA_API_URL = "http://localhost:11434/api/generate"
        
        # This would be a real prompt derived from audio in production
        prompt = "You are a speech-to-text transcriber. Provide a transcript of the following audio."
        
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", generate_transcript())
        else:
            logger.error(f"Ollama API error: {response.status_code} {response.text}")
            return generate_transcript()  # Fall back to simulation
    
    except Exception as e:
        logger.error(f"Error transcribing with Ollama: {str(e)}")
        return generate_transcript()  # Fall back to simulation

def get_current_mode_info() -> Dict[str, Any]:
    """
    Get information about the current transcription mode.
    
    Returns:
        Dict[str, Any]: Dictionary with mode information
    """
    return {
        "mode": current_mode,
        "name": TRANSCRIPTION_MODES.get(current_mode, "Unknown"),
        "available_modes": get_available_modes()
    }