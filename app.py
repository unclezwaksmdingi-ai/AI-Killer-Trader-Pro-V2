from flask import Flask, jsonify
import requests

app = Flask(__name__)

NTFY_TOPIC = "killer-trader-signals"

@app.route("/")
def home():
    return jsonify({"status": "AI Killer Trader Pro V2 Online"})

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
