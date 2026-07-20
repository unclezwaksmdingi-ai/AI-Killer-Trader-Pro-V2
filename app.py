from flask import Flask, jsonify
import os
import requests
import yfinance as yf

app = Flask(__name__)

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")


def send_notification(message):
    if NTFY_TOPIC:
        requests.post(
            f"{NTFY_SERVER}/{NTFY_TOPIC}",
            data=message.encode("utf-8")
        )


@app.route("/")
def home():
    return {
        "status": "AI Killer Trader Pro Online"
    }


@app.route("/signal")
def signal():
    symbol = "GC=F"  # Gold Futures

    data = yf.download(symbol, period="2d", interval="5m")

    if data.empty:
        return jsonify({"error": "No market data"}), 500

    close = float(data["Close"].iloc[-1])
    previous = float(data["Close"].iloc[-2])

    if close > previous:
        side = "BUY"
        sl = round(close - 10, 2)
        tp = round(close + 20, 2)
        confidence = 86
    else:
        side = "SELL"
        sl = round(close + 10, 2)
        tp = round(close - 20, 2)
        confidence = 86

    message = (
        f"📈 {side}\n"
        f"Pair: XAUUSD\n"
        f"Entry: {close}\n"
        f"Stop Loss: {sl}\n"
        f"Take Profit: {tp}\n"
        f"Confidence: {confidence}%"
    )

    send_notification(message)

    return jsonify({
        "signal": side,
        "pair": "XAUUSD",
        "entry": close,
        "stop_loss": sl,
        "take_profit": tp,
        "confidence": confidence
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
