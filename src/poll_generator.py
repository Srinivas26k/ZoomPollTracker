import random
import json
import logging
import re
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# This module simulates interaction with Ollama/Llama 3.2
# Since we're simulating, we'll use predefined templates and patterns

# Dictionary of topics and potential poll questions with options
POLL_TEMPLATES = {
    "project": {
        "questions": [
            "What's the biggest challenge facing our current project?",
            "Which area of the project needs the most attention?",
            "How confident are you about meeting the project deadline?",
            "What additional resources would most benefit the project?",
            "Which project milestone are you most concerned about?"
        ],
        "options": {
            "challenges": [
                "Resource constraints", 
                "Technical complexity", 
                "Timeline pressure", 
                "Stakeholder expectations"
            ],
            "areas": [
                "Backend development", 
                "Frontend UI/UX", 
                "Testing and QA", 
                "Documentation"
            ],
            "confidence": [
                "Very confident", 
                "Somewhat confident", 
                "Slightly concerned", 
                "Very concerned"
            ],
            "resources": [
                "Additional developers", 
                "More testing time", 
                "Better documentation", 
                "Improved collaboration tools"
            ],
            "milestones": [
                "Initial prototype", 
                "Feature complete", 
                "User acceptance testing", 
                "Final deployment"
            ]
        }
    },
    "marketing": {
        "questions": [
            "Which marketing channel has been most effective?",
            "What's the primary obstacle in our current marketing strategy?",
            "Which audience segment should we focus on next?",
            "How would you rate our brand messaging consistency?",
            "What type of content drives the most engagement?"
        ],
        "options": {
            "channels": [
                "Social media", 
                "Email campaigns", 
                "Content marketing", 
                "Paid advertising"
            ],
            "obstacles": [
                "Budget limitations", 
                "Market saturation", 
                "Messaging inconsistency", 
                "Lack of data"
            ],
            "segments": [
                "Enterprise clients", 
                "Small businesses", 
                "Individual consumers", 
                "Educational institutions"
            ],
            "consistency": [
                "Very consistent", 
                "Mostly consistent", 
                "Somewhat inconsistent", 
                "Very inconsistent"
            ],
            "content": [
                "Video content", 
                "Blog articles", 
                "Case studies", 
                "Infographics"
            ]
        }
    },
    "product": {
        "questions": [
            "Which feature should we prioritize in the next release?",
            "What aspect of the product needs most improvement?",
            "How user-friendly is our current interface?",
            "Which competitor feature should we consider implementing?",
            "What's the most valuable aspect of our product?"
        ],
        "options": {
            "features": [
                "User authentication", 
                "Reporting dashboard", 
                "Mobile support", 
                "API integration"
            ],
            "improvements": [
                "Performance", 
                "User interface", 
                "Documentation", 
                "Customization options"
            ],
            "usability": [
                "Very intuitive", 
                "Mostly intuitive", 
                "Somewhat confusing", 
                "Very confusing"
            ],
            "competitor": [
                "Advanced analytics", 
                "Simplified workflow", 
                "Better integration", 
                "Enhanced security"
            ],
            "value": [
                "Ease of use", 
                "Comprehensive features", 
                "Reliability", 
                "Customer support"
            ]
        }
    },
    "team": {
        "questions": [
            "What would improve team collaboration?",
            "How productive are our current meetings?",
            "What type of team activity would you prefer?",
            "How would you rate internal communication?",
            "What skill development would most benefit the team?"
        ],
        "options": {
            "collaboration": [
                "Better communication tools", 
                "Clear role definition", 
                "Regular check-ins", 
                "Shared documentation"
            ],
            "meetings": [
                "Very productive", 
                "Somewhat productive", 
                "Slightly unproductive", 
                "Very unproductive"
            ],
            "activities": [
                "Virtual team building", 
                "Skill sharing workshop", 
                "Hackathon", 
                "Social gathering"
            ],
            "communication": [
                "Excellent", 
                "Good but could improve", 
                "Needs significant improvement", 
                "Poor"
            ],
            "skills": [
                "Technical skills", 
                "Project management", 
                "Communication", 
                "Leadership"
            ]
        }
    },
    "general": {
        "questions": [
            "What topic should we discuss in our next meeting?",
            "How effective was this meeting?",
            "What's your preferred meeting format?",
            "How often should we have these discussions?",
            "What would make these meetings more valuable?"
        ],
        "options": {
            "topics": [
                "Strategic planning", 
                "Process improvement", 
                "Team collaboration", 
                "Industry trends"
            ],
            "effectiveness": [
                "Very effective", 
                "Somewhat effective", 
                "Slightly ineffective", 
                "Not effective"
            ],
            "format": [
                "Short daily check-ins", 
                "Weekly detailed reviews", 
                "Biweekly planning sessions", 
                "Monthly strategy discussions"
            ],
            "frequency": [
                "Weekly", 
                "Biweekly", 
                "Monthly", 
                "As needed"
            ],
            "improvements": [
                "More focused agenda", 
                "Better time management", 
                "More participant involvement", 
                "Better follow-up actions"
            ]
        }
    }
}

def analyze_transcript_topic(transcript):
    """
    Analyze the transcript to determine the primary topic.
    This simulates what an AI model would do.
    
    Args:
        transcript (str): The meeting transcript
        
    Returns:
        str: The determined topic category
    """
    # Count keyword occurrences to determine the most likely topic
    topic_keywords = {
        "project": ["project", "timeline", "deadline", "milestone", "task", "development", "sprint", "backlog"],
        "marketing": ["marketing", "campaign", "audience", "brand", "social media", "content", "engagement"],
        "product": ["product", "feature", "release", "user experience", "interface", "functionality"],
        "team": ["team", "collaboration", "communication", "meeting", "member", "cooperation"],
        # General is the fallback
    }
    
    # Count matches for each topic
    topic_counts = {topic: 0 for topic in topic_keywords}
    
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            # Case insensitive count
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', transcript, re.IGNORECASE))
            topic_counts[topic] += count
    
    # Find the topic with the most keyword matches
    max_count = max(topic_counts.values())
    
    # If we have a clear winner
    if max_count > 0:
        for topic, count in topic_counts.items():
            if count == max_count:
                return topic
    
    # Default to general if no clear topic is found
    return "general"

def generate_poll_from_transcript(transcript):
    """
    Generate a poll based on the meeting transcript.
    This simulates what would be done by Ollama/Llama 3.2.
    
    Args:
        transcript (str): The meeting transcript
        
    Returns:
        dict: JSON-formatted poll with a question and options
    """
    logger.debug("Generating poll from transcript...")
    
    # Analyze the transcript to determine the primary topic
    topic = analyze_transcript_topic(transcript)
    logger.debug(f"Determined topic: {topic}")
    
    # Get poll templates for this topic
    templates = POLL_TEMPLATES.get(topic, POLL_TEMPLATES["general"])
    
    # Select a random question from the templates
    question_key = random.choice(list(templates["questions"]))
    question_index = templates["questions"].index(question_key)
    question = question_key
    
    # Determine which option set to use based on the question
    option_keys = list(templates["options"].keys())
    option_key = option_keys[min(question_index, len(option_keys) - 1)]
    options = templates["options"][option_key]
    
    # Create the poll JSON
    poll = {
        "question": question,
        "options": options,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic
    }
    
    logger.debug(f"Generated poll: {poll}")
    return poll
