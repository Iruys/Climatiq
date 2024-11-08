from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    # Fetch weather data from wttr.in API in JSON format
    try:
        response = requests.get(f'https://wttr.in/{city}?format=j1')
        response.raise_for_status()
        data = response.json()
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temperature = current_condition['temp_C']

        # Return a JSON response with weather info
        return jsonify({
            'city': city,
            'description': weather_desc,
            'temperature': f"{temperature}°C"
        })
    except requests.RequestException:
        return jsonify({'error': 'Could not fetch weather data. Please try again.'}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
