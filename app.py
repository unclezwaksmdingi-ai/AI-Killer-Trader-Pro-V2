from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.get("/")
def home():
    send_signal("🚀 AI Killer Trader Pro is now online!")
    return {"status": "AI Killer Trader Pro Online"}

@app.route("/signal")
def signal():
    data = {
        "signal": "BUY",
        "pair": "XAUUSD",
        "confidence": 92
    }

    message = f"{data['signal']} {data['pair']} ({data['confidence']}%)"

    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8")
    )

    return jsonify(data)
import os
import requests

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")

def send_signal(message):
    if NTFY_TOPIC:
        requests.post(
            f"{NTFY_SERVER}/{NTFY_TOPIC}",
            data=message.encode("utf-8")
        )
