from app import app
import logging

if __name__ == "__main__":
    # Set up logging for easier debugging
    logging.basicConfig(level=logging.DEBUG)
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
