# server.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")  # Set this in Render

@app.route('/webhook', methods=['POST'])
def send_webhook():
    data = request.json
    content = {
        "embeds": [
            {
                "title": f"{data['type'].upper()} Message",
                "color": 16711680 if data["type"] == "user" else 65280,
                "fields": [
                    {"name": "Content", "value": data["content"][:1024]},
                    {"name": "IP", "value": data["ip"]},
                    {"name": "Location", "value": data["location"]},
                    {"name": "User Agent", "value": data["userAgent"]},
                    {"name": "Time", "value": data["time"]}
                ]
            }
        ]
    }
    r = requests.post(WEBHOOK, json=content)
    return jsonify({"status": "sent", "discord_status": r.status_code})

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    print(f"[LOG] {data['ip']}: {data['content']}")
    return jsonify({"status": "logged"})

if __name__ == '__main__':
    app.run(debug=False, port=5050)
