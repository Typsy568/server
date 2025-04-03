from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not WEBHOOK_URL:
        return "Webhook URL not configured", 500

    embed = {
        "embeds": [
            {
                "title": f"{data.get('type', 'UNKNOWN').upper()} Message",
                "color": 16711680 if data.get("type") in ["user", "user_file"] else 65280,
                "fields": [
                    {"name": "Content", "value": data.get("content", "N/A")},
                    {"name": "Info1", "value": data.get("ip", "unknown")},
                    {"name": "Info2", "value": data.get("location", "unknown")},
                    {"name": "Info3", "value": data.get("userAgent", "unknown")},
                    {"name": "Time", "value": data.get("time", "unknown")}
                ]
            }
        ]
    }
    r = requests.post(WEBHOOK_URL, json=embed)
    return jsonify({"status": "sent", "code": r.status_code})

@app.route("/log", methods=["POST"])
def log():
    print("[LOG]", request.json)
    return jsonify({"status": "logged"})

@app.route("/", methods=["GET"])
def health():
    return "Flask service online."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
