# Installation Guide

## Prerequisites

Before installing the Zoom Poll Automation system, ensure you have:

1. **Python 3.10 or newer** installed on your system
2. **pip** (Python package installer)
3. **Git** (optional, for cloning the repository)

## Dependencies

The application requires the following Python packages:

- Flask
- Flask-SocketIO
- email-validator
- flask-sqlalchemy
- gunicorn
- openai (optional, for OpenAI integration)
- psycopg2-binary
- python-dotenv
- requests
- trafilatura
- zoomus

## Windows Installation

### Step 1: Clone or Download the Repository

```
git clone https://github.com/yourusername/zoom-poll-automation.git
cd zoom-poll-automation
```

Or download and extract the ZIP file manually.

### Step 2: Set Up a Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```
pip install Flask==2.2.3 Flask-SocketIO==5.3.2 email-validator==2.0.0 flask-sqlalchemy==3.0.3 gunicorn==23.0.0 python-dotenv==1.0.0 requests==2.28.2 trafilatura==1.6.1 zoomus==1.1.5
```

For OpenAI integration (optional):

```
pip install openai==1.1.1
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root with the following content:

```
# Flask configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Zoom API credentials (optional, for real integration)
ZOOM_API_KEY=your_zoom_api_key
ZOOM_API_SECRET=your_zoom_api_secret
ZOOM_JWT_TOKEN=your_zoom_jwt_token

# OpenAI API key (optional)
OPENAI_API_KEY=your_openai_api_key
```

## macOS/Linux Installation

### Step 1: Clone or Download the Repository

```
git clone https://github.com/yourusername/zoom-poll-automation.git
cd zoom-poll-automation
```

Or download and extract the ZIP file manually.

### Step 2: Set Up a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```
pip install Flask==2.2.3 Flask-SocketIO==5.3.2 email-validator==2.0.0 flask-sqlalchemy==3.0.3 gunicorn==23.0.0 python-dotenv==1.0.0 requests==2.28.2 trafilatura==1.6.1 zoomus==1.1.5
```

For OpenAI integration (optional):

```
pip install openai==1.1.1
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root with the following content:

```
# Flask configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Zoom API credentials (optional, for real integration)
ZOOM_API_KEY=your_zoom_api_key
ZOOM_API_SECRET=your_zoom_api_secret
ZOOM_JWT_TOKEN=your_zoom_jwt_token

# OpenAI API key (optional)
OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

### Using Flask Development Server

```
python main.py
```

Or:

```
flask run
```

### Using Gunicorn (macOS/Linux only)

```
gunicorn --bind 0.0.0.0:5000 --worker-class eventlet main:app
```

## Verification

Once the server is running, open your web browser and navigate to:

```
http://localhost:5000
```

You should see the Zoom Poll Automation interface.

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port by setting the `PORT` environment variable
   - Kill the process using the port: `lsof -i :5000` (macOS/Linux) or use Task Manager (Windows)

2. **Missing dependencies**
   - Check error messages for missing packages
   - Install them using pip: `pip install package_name`

3. **Environment variable issues**
   - Ensure your `.env` file is in the correct location
   - Check for typos in variable names
   - Restart the application after modifying the `.env` file

4. **Socket.IO connection issues**
   - Check browser console for websocket errors
   - Ensure your firewall/antivirus isn't blocking websocket connections
   - Try a different browser

## Next Steps

After successful installation, refer to the [User Guide](USER_GUIDE.md) for detailed usage instructions.