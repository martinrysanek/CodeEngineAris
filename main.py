from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import urllib.request
import os

app = Flask(__name__)

import logging

class StringHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_output = ""

    def emit(self, record):
        log_message = self.format(record)
        self.log_output += log_message + "\n"
        
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get the current timestamp in a specific format
        timestamp = self.formatTime(record, datefmt='%Y-%m-%d %H:%M:%S')
        # custom_format = f"[{timestamp}] [{record.levelname}] {record.name}: {record.message}"
        custom_format = f"[{timestamp}] [{record.levelname}]: {record.message} <BR>"
        return custom_format

# Function to traverse the entire XML tree and display attributes of a given tag name
def find_and_display_attributes(element, tag_name):
    if element.tag.endswith(tag_name):
        text = element.text
        if text:
            # print(f"{tag_name} text: {text}")                
            return text
        else:
            return "Unknown"
    for child in element:
        name = find_and_display_attributes(child, tag_name)  
        if name != "Unknown":
            return name
    return "Unknown"


# set up root route
@app.route("/log", methods=['GET'])
def log():
    global string_handler
    # Retrieve the log messages as a single string
    html_in = "<HTML><BODY>"
    html_out = "</BODY></HTML>"
    return (html_in + string_handler.log_output + html_out)

# set up root route
@app.route("/", methods=['GET'])
def aris():
  global logger
  logger.debug("GET /")
  # url = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico=14890992'
  url = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico='
  ico_string = request.args.get('ico')  
  if not ico_string.isdigit():
      return "Not valid ICO format"
  logger.debug("ICO: " + ico_string)
  response = urllib.request.urlopen(url+ico_string.strip())
  data = response.read()
  # Parse the XML string
  root = ET.fromstring(data)
  # Example: Display all attributes for the 'person' tag throughout the XML tree
  name = find_and_display_attributes(root, 'OF')
  logger.debug("NAME: " + name)
  return name

# Configure logging with a custom log message format
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Format for the timestamp
)

# Create a logger
logger = logging.getLogger(__name__)

# Create a custom formatter
custom_formatter = CustomFormatter()

# Create a custom logging handler to capture log messages in a string
string_handler = StringHandler()
string_handler.setFormatter(custom_formatter)
logger.addHandler(string_handler)

# Log some messages
logger.debug("This is a debug message")
logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")

# Get the PORT from environment
port = os.getenv('PORT', '8080')
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=int(port))


