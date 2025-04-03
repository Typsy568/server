import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="static")
CORS(app)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    if not WEBHOOK_URL:
        return jsonify({"error": "Webhook URL not set"}), 500

    requests.post(WEBHOOK_URL, json={
        "embeds": [
            {
                "title": f"{data['type'].upper()} Message",
                "color": 16711680 if data["type"] == "user" else 65280,
                "fields": [
                    {"name": "Message", "value": data["content"][:1024]},
                    {"name": "Client Info", "value": f"{data['location']} | {data['userAgent']}"},
                    {"name": "Time", "value": data["time"]}
                ]
            }
        ]
    })
    return jsonify({"status": "sent"})

@app.route("/log", methods=["POST"])
def handle_log():
    data = request.json
    print("Log:", data)
    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run()
