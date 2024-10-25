from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import os
import logging
pip install google.generativeai
app = Flask(__name__, static_folder='.')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configuration
import google.generativeai as genai

genai.configure(api_key="AIzaSyBWLGfhjfsWIS2QQWi4a7MxbB_gsf-4h58")
model = genai.GenerativeModel("gemini-1.5-flash")
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/identify-plant', methods=['POST'])
def identify_plant():
    try:
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            app.logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400
        
        if file:
            # Read the image file
            img_data = file.read()
            
            # Encode the image to base64
            base64_img = base64.b64encode(img_data).decode('ascii')
            
            # Prepare the data for the Plant.id API
            data = {
                "api_key": API_KEY,
                "images": [base64_img],
                "modifiers": ["crops_fast", "similar_images"],
                "plant_language": "en",
                "plant_details": ["common_names", "url", "wiki_description", "taxonomy"]
            }
            
            # Make a request to the Plant.id API
            app.logger.info("Sending request to Plant.id API")
            response = requests.post(PLANT_ID_API_ENDPOINT, json=data)
            result = response.json()
            
            if response.status_code == 200 and result.get('suggestions'):
                plant = result['suggestions'][0]
                
                # Format the response
                formatted_response = {
                    "name": plant['plant_name'],
                    "info": plant['plant_details']['wiki_description']['value'],
                    "medicinalUse": get_medicinal_use(plant['plant_name'])
                }
                
                app.logger.info(f"Plant identified: {plant['plant_name']}")
                return jsonify(formatted_response)
            else:
                app.logger.error(f"Plant.id API error: {result.get('error')}")
                return jsonify({"error": "Unable to identify the plant"}), 500
        
        app.logger.error("Unexpected error occurred")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
    except Exception as e:
        app.logger.exception(f"Exception occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

def get_medicinal_use(plant_name):
    # This is a placeholder function. In a real-world scenario, 
    # you would query a database or another API for this information.
    return f"Medicinal uses for {plant_name} vary. Please consult with a healthcare professional before using any plant for medicinal purposes."

if __name__ == '__main__':
    app.run(debug=True)
