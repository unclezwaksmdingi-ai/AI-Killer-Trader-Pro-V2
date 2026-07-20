from flask import Flask, jsonify
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Gmail settings
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO", EMAIL_ADDRESS)


def send_email(subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Missing EMAIL_ADDRESS or EMAIL_PASSWORD")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Email error: {e}")


@app.route("/")
def home():
    send_email(
        "🚀 AI Killer Trader Pro",
        "Your AI Killer Trader Pro is now online and running on Render."
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
🔥 AI Killer Trader Signal

Signal: {data['signal']}
Pair: {data['pair']}
Confidence: {data['confidence']}%

Good luck!
"""

    send_email("📈 New Trading Signal", message)

    return jsonify(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
