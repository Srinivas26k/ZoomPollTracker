import random
import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Sample meeting topics for random transcript generation
MEETING_TOPICS = [
    "Project Status Update",
    "Marketing Strategy Discussion",
    "Product Development Roadmap",
    "Customer Feedback Review",
    "Team Building Activities",
    "Budget Planning for Next Quarter",
    "New Feature Implementation",
    "User Experience Improvements",
    "Sales Performance Review",
    "Technical Architecture Discussion"
]

# Sample phrases for each topic to make transcripts more realistic
TOPIC_PHRASES = {
    "Project Status Update": [
        "The project is on track for the deadline.",
        "We need to address the delay in the backend development.",
        "QA testing is showing positive results so far.",
        "The client is happy with our progress.",
        "We should focus on completing the high-priority features first.",
        "Let's review the timeline for the remaining tasks.",
        "There are some bottlenecks in the development process we need to resolve.",
        "The team has been working overtime to catch up on deliverables.",
        "Our burndown chart indicates we might need another sprint for completion.",
        "Documentation is keeping pace with development."
    ],
    "Marketing Strategy Discussion": [
        "The social media campaign is performing well above expectations.",
        "Our email marketing open rates have decreased in the last month.",
        "We should target a new demographic based on recent market research.",
        "The budget allocation for digital ads needs revision.",
        "Competitor analysis shows an opportunity in the B2B sector.",
        "Customer acquisition costs are too high for the current strategy.",
        "Let's focus on retargeting campaigns for better ROI.",
        "Content marketing is driving significant organic traffic.",
        "We need to align our messaging across all channels.",
        "The new brand guidelines have been well-received by focus groups."
    ],
    "Product Development Roadmap": [
        "The next feature release should prioritize user-requested features.",
        "We need to decide between improving existing features or adding new ones.",
        "The tech debt is starting to impact development velocity.",
        "Let's plan for a major version upgrade in Q3.",
        "API improvements should be scheduled before the UI enhancements.",
        "We've been receiving requests for better mobile support.",
        "Performance optimization should be a cross-cutting concern for all teams.",
        "Security vulnerabilities need immediate attention in the next sprint.",
        "The prototype for the new dashboard has received positive feedback.",
        "Integration with third-party services is becoming a priority for clients."
    ],
    "Customer Feedback Review": [
        "Users are consistently requesting a dark mode for the application.",
        "The most recent survey shows high satisfaction with customer support.",
        "Performance complaints have decreased since our last optimization sprint.",
        "Mobile users are reporting issues with the checkout process.",
        "The new feature has received mixed feedback, with some confusion about its purpose.",
        "Enterprise clients are requesting more customization options.",
        "We've seen an increase in positive reviews on the app store.",
        "The help documentation needs updating based on common support tickets.",
        "User testing revealed navigation issues in the dashboard interface.",
        "Several customers have suggested integrations with productivity tools."
    ],
    "Team Building Activities": [
        "The virtual escape room was a great success for remote team bonding.",
        "We should schedule the next team outing for the end of the quarter.",
        "The mentorship program has received positive feedback from participants.",
        "Let's introduce a weekly informal coffee chat to improve team communication.",
        "The cross-department hackathon fostered collaboration and innovation.",
        "Team satisfaction surveys show improvement after implementing flexible work hours.",
        "We need more activities that include our international team members.",
        "The skill-sharing workshops have been well-attended and valuable.",
        "Recognition programs are helping with team morale and motivation.",
        "The annual retreat planning is underway with a focus on strategic alignment."
    ],
    "Budget Planning for Next Quarter": [
        "We need to increase the development budget to accommodate the new project.",
        "Marketing expenses exceeded projections but delivered strong results.",
        "Cloud infrastructure costs are growing faster than anticipated.",
        "Let's review the ROI on our current software subscriptions.",
        "The training budget has been underutilized this quarter.",
        "We should allocate more resources to security and compliance.",
        "Customer acquisition costs have decreased due to improved targeting.",
        "The hiring freeze will impact our capacity in the coming months.",
        "Equipment upgrades should be prioritized for the design team.",
        "Travel expenses will likely increase as in-person events resume."
    ],
    "New Feature Implementation": [
        "The authentication system needs redesigning to support SSO.",
        "We should implement the reporting dashboard in phases for faster delivery.",
        "API rate limiting is essential for the upcoming high-traffic feature.",
        "The data export functionality requires additional file format options.",
        "Mobile responsiveness should be tested across all major device types.",
        "Let's prioritize accessibility improvements in this release.",
        "The notification system needs customization options for different user roles.",
        "We've finalized the design for the drag-and-drop interface.",
        "Error handling for edge cases needs more robust implementation.",
        "Performance testing indicates we need to optimize database queries."
    ],
    "User Experience Improvements": [
        "The onboarding flow is confusing for new users according to heatmap data.",
        "Form validation messages should be more descriptive and helpful.",
        "We need to reduce the number of clicks to complete common tasks.",
        "User testing revealed issues with icon comprehension in the toolbar.",
        "Loading states should be added to all asynchronous operations.",
        "The color contrast doesn't meet accessibility standards in some areas.",
        "Navigation restructuring has improved task completion rates in testing.",
        "Mobile gesture support would enhance the touch experience significantly.",
        "Empty states need redesigning to provide more guidance.",
        "Tooltip content should be revised for clarity and brevity."
    ],
    "Sales Performance Review": [
        "Q1 targets were exceeded by 15% in the enterprise segment.",
        "The new pricing model has increased average deal size by 20%.",
        "Sales cycle length has decreased after implementing the new CRM features.",
        "We should reconsider our approach to the SMB market based on recent data.",
        "Customer retention rates are improving but still below industry benchmarks.",
        "The sales enablement materials need updating with the latest use cases.",
        "Partner channel sales are growing faster than direct sales this quarter.",
        "Discounting practices vary widely across the sales team and need standardization.",
        "Trial conversion rates are higher for accounts with active onboarding support.",
        "The sales territory realignment has reduced overlap and increased efficiency."
    ],
    "Technical Architecture Discussion": [
        "We should consider moving to a microservices architecture for better scalability.",
        "The current database structure won't support our projected growth.",
        "Cache implementation is needed to improve response times for frequent queries.",
        "API versioning strategy needs revision to avoid breaking client integrations.",
        "We should evaluate serverless options for cost optimization.",
        "The monolithic backend is becoming difficult to maintain and update.",
        "Security review identified potential vulnerabilities in our authentication flow.",
        "Let's discuss the pros and cons of container orchestration solutions.",
        "Data replication lag is causing inconsistencies in distributed systems.",
        "The CI/CD pipeline needs optimization to reduce build times."
    ]
}

# Participant names for transcript simulation
PARTICIPANT_NAMES = [
    "Alex", "Taylor", "Jordan", "Morgan", "Casey", 
    "Sam", "Riley", "Jamie", "Drew", "Bailey", 
    "Chris", "Logan", "Quinn", "Skyler", "Avery"
]

def generate_transcript():
    """
    Generate a simulated meeting transcript.
    
    Returns:
        str: A simulated 10-minute meeting transcript.
    """
    logger.debug("Generating simulated transcript...")
    
    # Select a random meeting topic
    topic = random.choice(MEETING_TOPICS)
    
    # Select 3-5 random participants
    num_participants = random.randint(3, 5)
    participants = random.sample(PARTICIPANT_NAMES, num_participants)
    
    # Generate a transcript with timestamps
    transcript_lines = []
    
    # Start time between 10 and 30 minutes ago
    start_time = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(10, 30))
    current_time = start_time
    
    # Introduction
    transcript_lines.append(f"{current_time.strftime('%H:%M:%S')} - Meeting started: {topic} Discussion")
    current_time += datetime.timedelta(seconds=random.randint(10, 30))
    
    # Add host introduction
    host = random.choice(participants)
    transcript_lines.append(f"{current_time.strftime('%H:%M:%S')} - {host}: Welcome everyone to our {topic} meeting. Let's get started.")
    current_time += datetime.timedelta(seconds=random.randint(5, 15))
    
    # Generate random discussion for about 10 minutes of transcript
    topic_phrases = TOPIC_PHRASES[topic]
    
    for _ in range(15):  # Generate 15 conversation exchanges
        speaker = random.choice(participants)
        
        # Select 1-3 phrases to combine
        num_phrases = random.randint(1, 3)
        selected_phrases = random.sample(topic_phrases, num_phrases)
        message = " ".join(selected_phrases)
        
        transcript_lines.append(f"{current_time.strftime('%H:%M:%S')} - {speaker}: {message}")
        
        # Random time increment between messages
        current_time += datetime.timedelta(seconds=random.randint(20, 60))
    
    # Add some reactions and questions
    for _ in range(5):  # Add 5 reactions/questions
        speaker = random.choice(participants)
        reactions = [
            "I agree with that point. We should definitely pursue this further.",
            "I'm not sure if that will work with our current constraints.",
            "Can we discuss this in more detail next week?",
            "That's an interesting perspective. I hadn't thought of it that way.",
            "Could you explain how that would affect our existing systems?",
            "I think we need more data before making that decision.",
            "Let's set up a follow-up meeting to dive deeper into this topic.",
            "Does anyone have concerns about this approach?",
            "Great point! This aligns well with our strategic goals.",
            "I'd like to suggest an alternative solution if I may."
        ]
        
        transcript_lines.append(f"{current_time.strftime('%H:%M:%S')} - {speaker}: {random.choice(reactions)}")
        current_time += datetime.timedelta(seconds=random.randint(15, 45))
    
    # Add a conclusion
    concluding_speaker = random.choice(participants)
    conclusion = f"{current_time.strftime('%H:%M:%S')} - {concluding_speaker}: I think we've covered a lot today. Let's summarize our action items and next steps."
    transcript_lines.append(conclusion)
    
    # Join all lines with newlines
    transcript = "\n".join(transcript_lines)
    
    logger.debug(f"Generated transcript with {len(transcript_lines)} lines on topic: {topic}")
    return transcript
