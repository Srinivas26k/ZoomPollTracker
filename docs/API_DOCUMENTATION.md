# Zoom Poll Automation API Documentation

This document provides comprehensive information about the APIs available in the Real-Time Zoom Poll Automation application for developers and integrators.

## Overview

The Zoom Poll Automation system provides several REST API endpoints for integration and customization. These APIs allow you to:

1. Retrieve and generate polls
2. Select AI models for poll generation and transcription
3. Manage poll generation intervals
4. Retrieve model information and available options

## Authentication

All API requests require a valid session. Authentication is handled through Zoom OAuth for application permissions.

## Base URL

All API endpoints are relative to your application's base URL:

```
https://your-server-domain.com/api/
```

## Endpoints

### Poll Management

#### Get Current Poll

Retrieves the current active poll and related information.

- **URL**: `/api/get-poll`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "success": true,
    "poll": {
      "question": "How would you rate team collaboration?",
      "options": ["Excellent", "Good", "Fair", "Poor"],
      "generated_at": "2025-04-14 09:15:30",
      "topic": "team"
    },
    "transcript": "Meeting transcript content...",
    "timestamp": "2025-04-14 09:15:30",
    "timeUntilNext": 850
  }
  ```

#### Generate New Poll

Generates a new poll immediately.

- **URL**: `/api/generate-poll`
- **Method**: `POST`
- **Response**:
  ```json
  {
    "success": true,
    "poll": {
      "question": "Which feature should we prioritize?",
      "options": ["Feature A", "Feature B", "Feature C", "Feature D"],
      "generated_at": "2025-04-14 09:20:15",
      "topic": "product"
    },
    "transcript": "Meeting transcript content...",
    "timestamp": "2025-04-14 09:20:15",
    "model_info": {
      "model_key": "openai",
      "name": "OpenAI GPT-4o",
      "description": "Advanced cloud AI model with broad capabilities",
      "local": false
    }
  }
  ```

#### Update Poll Interval

Changes the frequency of automatic poll generation.

- **URL**: `/api/update-interval`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "interval": 900
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Interval updated to 900 seconds"
  }
  ```

### AI Model Management

#### Get Available Models

Retrieves information about available AI models and options.

- **URL**: `/api/models`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "success": true,
    "current_model": {
      "model_key": "openai",
      "name": "OpenAI GPT-4o",
      "description": "Advanced cloud AI model with broad capabilities",
      "local": false
    },
    "available_models": {
      "openai": {
        "name": "OpenAI GPT-4o",
        "description": "Advanced cloud AI model with broad capabilities",
        "local": false
      },
      "ollama_llama3": {
        "name": "Ollama llama3.2:3b",
        "description": "Lightweight open-source LLM for local processing",
        "local": true
      },
      "simulation": {
        "name": "Simulation (Testing)",
        "description": "Uses pre-defined templates for testing",
        "local": true
      }
    },
    "available_transcription": {
      "openai": "OpenAI Whisper API (Cloud)",
      "simulation": "Simulated Transcription (Testing)"
    }
  }
  ```

#### Set Poll Generation Model

Changes the AI model used for poll generation.

- **URL**: `/api/models/poll`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "model": "ollama_llama3"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Poll generation model set to ollama_llama3",
    "current_model": {
      "model_key": "ollama_llama3",
      "name": "Ollama llama3.2:3b",
      "description": "Lightweight open-source LLM for local processing",
      "local": true
    }
  }
  ```

#### Set Transcription Mode

Changes the method used for meeting transcription.

- **URL**: `/api/models/transcription`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "mode": "openai"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Transcription mode set to openai",
    "available_modes": {
      "openai": "OpenAI Whisper API (Cloud)",
      "simulation": "Simulated Transcription (Testing)"
    }
  }
  ```

## WebSocket Events

The application also provides real-time updates through WebSocket events.

### Poll Update Event

Sent when a new poll is generated:

```json
{
  "event": "poll_update",
  "data": {
    "poll": {
      "question": "What aspect of the product needs most improvement?",
      "options": ["Performance", "User interface", "Documentation", "Customization options"],
      "generated_at": "2025-04-14 09:30:45",
      "topic": "product"
    },
    "transcript": "Meeting transcript content...",
    "timestamp": "2025-04-14 09:30:45"
  }
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a descriptive message:

```json
{
  "success": false,
  "message": "Error details here"
}
```

## Rate Limiting

To ensure system stability, API requests are limited to 100 requests per minute per client.

## Integration Examples

### JavaScript Example

```javascript
// Generate a new poll
async function generateNewPoll() {
  const response = await fetch('/api/generate-poll', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('New poll generated:', data.poll.question);
  } else {
    console.error('Error generating poll:', data.message);
  }
}

// Set poll generation model
async function setAIModel(modelKey) {
  const response = await fetch('/api/models/poll', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: modelKey
    })
  });
  
  const data = await response.json();
  return data.success;
}
```

### Python Example

```python
import requests

# API base URL
BASE_URL = 'https://your-server-domain.com/api'

# Get available models
def get_available_models():
    response = requests.get(f'{BASE_URL}/models')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Update poll interval
def update_interval(seconds):
    response = requests.post(
        f'{BASE_URL}/update-interval',
        json={'interval': seconds}
    )
    return response.json()
```