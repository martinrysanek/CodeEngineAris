from flask import Flask
import xml.etree.ElementTree as ET
import urllib.request
import os

app = Flask(__name__)

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
@app.route("/")
def aris():
  url = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico=14890992'
  response = urllib.request.urlopen(url)
  data = response.read()
  # Parse the XML string
  root = ET.fromstring(data)
  # Example: Display all attributes for the 'person' tag throughout the XML tree
  name = find_and_display_attributes(root, 'OF')
  return name

# Get the PORT from environment
port = os.getenv('PORT', '8080')
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=int(port))
