from flask import Flask, render_template, request, redirect, url_for
import os, json
import logging
from datetime import datetime
from urllib.parse import parse_qs

# Initialize the Flask application
app = Flask(__name__) 

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the path to the data file
DATA_FILE = os.path.join('storage', 'data.json')

# Function to load data from the JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        logger.debug("Data file does not exist. Returning empty dictionary.")
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            logger.debug("Data loaded successfully.")
            return data
        except json.JSONDecodeError:
            logger.error("JSON decode error. Returning empty dictionary.")
            return {}
# Function to save data to the JSON file
def save_data(message_dict):
    data = load_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data[timestamp] = message_dict
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.debug(f"Data saved successfully at {timestamp}.")

# Route for the index page
@app.route('/')
def index():
    logger.debug("Rendering index page.")
    return render_template('index.html')

# Route for handling messages
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        data_bytes = request.get_data()
        data_str = data_bytes.decode('utf-8')
        parsed = parse_qs(data_str)
        message_dict = {key: value[0] for key, value in parsed.items()}
        save_data(message_dict)
        logger.debug("Message received and saved.")
        return redirect(url_for('index'))
    logger.debug("Rendering message page.")    
    return render_template('message.html')

# Route for reading messages
@app.route('/read')
def read_messages():
    messages = load_data()
    logger.debug("Rendering read messages page.")
    return render_template('read.html', messages=messages)

# Error handler for 404 errors
@app.errorhandler(404)
def page_not_found(_error):
    logger.error("Page not found: 404 error.")
    return render_template('error.html'), 404

# Main entry point of the application
if __name__ == '__main__':
    # Create storage directory if it does not exist
    if not os.path.exists('storage'):
        os.makedirs('storage')
        logger.debug("Storage directory created.")
    # Create data file if it does not exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
            logger.debug("Data file created.")
    logger.debug("Starting Flask app.")
    # Run the Flask application
    app.run(port=3000, debug=True)
