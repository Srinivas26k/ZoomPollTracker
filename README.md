# Real-Time Zoom Poll Automation

## Overview
This project is a proof-of-concept for automating poll generation during a live Zoom meeting. It simulates capturing a 10-minute transcript, generating a poll using a local instance of Ollama's Llama 3.2, and posting the poll into a simulated Zoom meeting UI every 15 minutes.

## Features
- **Transcript Capture Simulation:** Dummy transcript generator that creates realistic meeting conversations.
- **AI-Powered Poll Generation:** Simulates using a local Llama 3.2 model (via Ollama) to create poll questions and options based on the meeting content.
- **Automated Poll Posting:** Simulated Zoom meeting integration with custom UI to display generated polls.
- **Real-time Updates:** Uses WebSockets to push new polls to the UI without requiring page refresh.
- **Configurable Polling Interval:** Customize how frequently polls are generated (default: 15 minutes).
- **Completely Free:** All components are free/open-source for local testing.

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- Flask and other dependencies (see below)

### Installation

1. Clone the repository:
   