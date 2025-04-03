from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route('/')
def index():
    return 'Flask service online.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or not DISCORD_WEBHOOK_URL:
        return jsonify({'error': 'Missing data or webhook URL'}), 400

    content = {
        "embeds": [
            {
                "title": f"{data.get('type', 'Unknown').upper()} Message",
                "color": 16711680 if data.get('type') == 'user' else 65280,
                "fields": [
                    {"name": "Content", "value": data.get('content', 'N/A')[:1024]},
                    {"name": "IP", "value": data.get('ip', 'N/A')},
                    {"name": "Location", "value": data.get('location', 'N/A')},
                    {"name": "User Agent", "value": data.get('userAgent', 'N/A')},
                    {"name": "Time", "value": data.get('time', 'N/A')}
                ]
            }
        ]
    }

    requests.post(DISCORD_WEBHOOK_URL, json=content)
    return jsonify({'status': 'sent'}), 200

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    print("Logged:", data)
    return jsonify({"status": "logged"}), 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)
