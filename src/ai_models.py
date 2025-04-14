"""
AI model management for poll generation and transcript analysis.
Provides a unified interface for using different AI models with fallback options.
"""

import os
import logging
import json
import requests
from typing import Dict, List, Any, Optional
import random
from datetime import datetime

# Import local modules
from src.poll_generator import generate_poll_from_transcript
from src.transcription import transcribe_audio, set_transcription_mode, get_available_modes

# Set up logging
logger = logging.getLogger(__name__)

# Check for OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Available models for poll generation
POLL_GENERATION_MODELS = {
    "openai": {
        "name": "OpenAI GPT-4o",
        "description": "Advanced cloud AI model with broad capabilities (requires API key)",
        "local": False
    },
    "ollama_llama3": {
        "name": "Ollama llama3.2:3b",
        "description": "Lightweight open-source LLM for local processing",
        "local": True
    },
    "gemini": {
        "name": "Google Gemini",
        "description": "Google's advanced model for content generation (requires API key)",
        "local": False
    },
    "mistral": {
        "name": "Mistral",
        "description": "Efficient open-source model with strong reasoning (requires API key)",
        "local": False
    },
    "simulation": {
        "name": "Simulation (Testing)",
        "description": "Uses pre-defined templates for testing (no AI required)",
        "local": True
    }
}

# Default to simulation if no API keys are available
DEFAULT_POLL_MODEL = "openai" if OPENAI_API_KEY else "simulation"
current_poll_model = DEFAULT_POLL_MODEL

def set_poll_model(model_key: str) -> bool:
    """
    Set the AI model to use for poll generation.
    
    Args:
        model_key (str): The key of the model to use
        
    Returns:
        bool: True if successful, False if model is invalid
    """
    global current_poll_model
    
    if model_key in POLL_GENERATION_MODELS:
        current_poll_model = model_key
        logger.info(f"Poll generation model set to: {POLL_GENERATION_MODELS[model_key]['name']}")
        return True
    else:
        logger.error(f"Invalid poll generation model: {model_key}")
        return False

def get_available_poll_models() -> Dict[str, Dict[str, Any]]:
    """
    Get a dictionary of available poll generation models.
    
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of available models with details
    """
    # Filter out unavailable models
    available_models = {}
    
    # OpenAI requires API key
    if OPENAI_API_KEY:
        available_models["openai"] = POLL_GENERATION_MODELS["openai"]
    
    # Check if Ollama is installed and available
    try:
        # This tests if we can connect to the Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
        if response.status_code == 200:
            # Check if llama3 model is available
            models = response.json().get("models", [])
            if any("llama3" in model.get("name", "") for model in models):
                available_models["ollama_llama3"] = POLL_GENERATION_MODELS["ollama_llama3"]
    except:
        # If Ollama is not available, don't add it to available models
        pass
    
    # Simulation is always available as fallback
    available_models["simulation"] = POLL_GENERATION_MODELS["simulation"]
    
    return available_models

def get_current_model_info() -> Dict[str, Any]:
    """
    Get information about the current poll generation model.
    
    Returns:
        Dict[str, Any]: Dictionary with model information
    """
    model_info = POLL_GENERATION_MODELS.get(current_poll_model, POLL_GENERATION_MODELS["simulation"])
    
    return {
        "model_key": current_poll_model,
        "name": model_info["name"],
        "description": model_info["description"],
        "local": model_info["local"],
        "available_models": get_available_poll_models(),
        "transcription": get_available_modes()
    }

def generate_poll(transcript: str) -> Dict[str, Any]:
    """
    Generate a poll based on meeting transcript using the selected AI model.
    
    Args:
        transcript (str): Meeting transcript
        
    Returns:
        Dict[str, Any]: Poll data
    """
    # Currently, we use the simulation regardless of the selected model
    # In a production implementation, this would branch based on current_poll_model
    
    if current_poll_model == "openai" and OPENAI_API_KEY:
        return generate_poll_with_openai(transcript)
    elif current_poll_model == "ollama_llama3":
        return generate_poll_with_ollama(transcript)
    else:
        # Fall back to simulated poll generation
        return generate_poll_from_transcript(transcript)

def generate_poll_with_openai(transcript: str) -> Dict[str, Any]:
    """
    Generate a poll using OpenAI GPT-4o.
    
    Args:
        transcript (str): Meeting transcript
        
    Returns:
        Dict[str, Any]: Poll data
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set, cannot use GPT-4o")
        return generate_poll_from_transcript(transcript)
    
    logger.info("Generating poll with OpenAI GPT-4o")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        system_prompt = """
        You are an expert at creating relevant polls for Zoom meetings.
        Analyze the meeting transcript and create a single poll question with multiple-choice options.
        The poll should be relevant to the meeting content and designed to gather meaningful feedback or insights.
        
        Return ONLY a JSON object with the following structure:
        {
            "question": "Your poll question here?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "topic": "identified_topic"
        }
        
        The topic should be one of: project, marketing, product, team, or general.
        Provide 4 options that are clear, concise, and cover the likely range of responses.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the meeting transcript to analyze:\n\n{transcript}"}
            ],
            response_format={"type": "json_object"}
        )
        
        poll_data = json.loads(response.choices[0].message.content)
        
        # Add generated_at timestamp
        poll_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Successfully generated poll with OpenAI: {poll_data['question']}")
        return poll_data
    
    except Exception as e:
        logger.error(f"Error generating poll with OpenAI: {str(e)}")
        # Fall back to simulation
        return generate_poll_from_transcript(transcript)

def generate_poll_with_ollama(transcript: str) -> Dict[str, Any]:
    """
    Generate a poll using local Ollama llama3.2:3b model.
    
    Args:
        transcript (str): Meeting transcript
        
    Returns:
        Dict[str, Any]: Poll data
    """
    logger.info("Generating poll with Ollama llama3.2")
    
    try:
        OLLAMA_API_URL = "http://localhost:11434/api/generate"
        
        prompt = f"""
        Create a relevant poll for a Zoom meeting based on this transcript:
        
        {transcript}
        
        Return your response as a JSON object with the following structure:
        {{
            "question": "Your poll question here?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "topic": "identified_topic"
        }}
        
        The topic should be one of: project, marketing, product, team, or general.
        Provide 4 options that are clear, concise, and cover the likely range of responses.
        """
        
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "llama3:3b",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            
            # Extract JSON object from response
            try:
                # Find JSON block in response - it might be surrounded by other text
                import re
                json_pattern = r'\{.*\}'
                json_match = re.search(json_pattern, response_text, re.DOTALL)
                
                if json_match:
                    poll_data = json.loads(json_match.group(0))
                    # Add generated_at timestamp
                    poll_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.info(f"Successfully generated poll with Ollama: {poll_data['question']}")
                    return poll_data
                else:
                    logger.error("Could not extract JSON from Ollama response")
                    return generate_poll_from_transcript(transcript)
            except json.JSONDecodeError:
                logger.error("Invalid JSON in Ollama response")
                return generate_poll_from_transcript(transcript)
        else:
            logger.error(f"Ollama API error: {response.status_code} {response.text}")
            return generate_poll_from_transcript(transcript)
    
    except Exception as e:
        logger.error(f"Error generating poll with Ollama: {str(e)}")
        # Fall back to simulation
        return generate_poll_from_transcript(transcript)