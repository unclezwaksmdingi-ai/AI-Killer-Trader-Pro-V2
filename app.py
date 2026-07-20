from flask import Flask, jsonify
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO", EMAIL_ADDRESS)


def send_email(subject, message):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email settings are missing.")
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Email error: {e}")


@app.route("/")
def home():
    send_email(
        "AI Killer Trader Pro",
        "🚀 AI Killer Trader Pro is now online!"
    )
    return jsonify({"status": "AI Killer Trader Pro Online"})


@app.route("/signal")
def signal():
    data = {
        "signal": "BUY",
        "pair": "XAUUSD",
        "confidence": 92
    }

    message = f"""
Trading Signal

Signal: {data['signal']}
Pair: {data['pair']}
Confidence: {data['confidence']}%
"""

    send_email("New Trading Signal", message)

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
