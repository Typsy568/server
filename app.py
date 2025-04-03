from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- allows frontend to talk to backend

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/")
def home():
    return "Flask service online."

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": f"{data.get('type', 'Message').upper()}",
                "fields": [
                    {"name": "Content", "value": data.get("content", "")},
                    {"name": "Location", "value": data.get("location", "Unknown")},
                    {"name": "User Agent", "value": data.get("userAgent", "Unknown")},
                    {"name": "Time", "value": data.get("time", "")}
                ]
            }]
        })
    return jsonify({"status": "sent"})

@app.route("/log", methods=["POST"])
def log_message():
    data = request.json
    print(f"[LOG] {data.get('ip')} -> {data.get('content')}")
    return jsonify({"status": "logged"})
