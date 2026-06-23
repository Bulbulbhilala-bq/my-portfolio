"""
Portfolio Backend - Flask API
Bulbul Bhilala Portfolio
Run: python app.py
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
import os          # ← load_dotenv ke BAAD
import re
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = "portfolio.db"

# ── Gmail Config ─────────────────────────────────────────────────
GMAIL_USER     = os.environ.get("GMAIL_USER", "bhilalabulbul32@gmail.com")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD", "")
NOTIFY_EMAIL   = os.environ.get("NOTIFY_EMAIL", "bhilalabulbul32@gmail.com")
print(f"DEBUG — Password loaded: {'YES ✅' if GMAIL_PASSWORD else 'NO ❌'}") 


def send_gmail(name, email, subject, message):
    """Send email notification to your Gmail."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📩 Portfolio Contact: {subject}"
        msg["From"]    = GMAIL_USER
        msg["To"]      = NOTIFY_EMAIL
        msg["Reply-To"] = email

        html = f"""
        <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
          <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
            <div style="background:linear-gradient(135deg,#0066ff,#00c8ff);padding:25px 30px;">
              <h2 style="color:#fff;margin:0;">📩 New Portfolio Message</h2>
              <p style="color:rgba(255,255,255,0.8);margin:5px 0 0;">From your portfolio contact form</p>
            </div>
            <div style="padding:30px;">
              <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:8px 0;color:#666;width:80px;"><b>Name</b></td><td style="padding:8px 0;color:#333;">{name}</td></tr>
                <tr><td style="padding:8px 0;color:#666;"><b>Email</b></td><td style="padding:8px 0;"><a href="mailto:{email}" style="color:#0066ff;">{email}</a></td></tr>
                <tr><td style="padding:8px 0;color:#666;"><b>Subject</b></td><td style="padding:8px 0;color:#333;">{subject}</td></tr>
              </table>
              <div style="margin-top:20px;padding:15px;background:#f8f9ff;border-left:4px solid #00c8ff;border-radius:4px;">
                <b style="color:#666;">Message:</b>
                <p style="color:#333;margin:8px 0 0;line-height:1.6;">{message.replace(chr(10), '<br>')}</p>
              </div>
              <div style="margin-top:25px;padding-top:20px;border-top:1px solid #eee;">
                <a href="mailto:{email}?subject=Re: {subject}" 
                   style="background:linear-gradient(135deg,#0066ff,#00c8ff);color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;">
                  Reply to {name} →
                </a>
              </div>
            </div>
            <div style="background:#f8f9ff;padding:15px 30px;text-align:center;">
              <p style="color:#999;font-size:12px;margin:0;">Bulbul Bhilala Portfolio — Auto Notification</p>
            </div>
          </div>
        </body></html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())

        print(f"✅ Email notification sent to {NOTIFY_EMAIL}")
        return True
    except Exception as e:
        print(f"⚠️  Email send failed: {e}")
        return False


# ── Database Setup ───────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL,
            subject  TEXT,
            message  TEXT    NOT NULL,
            received TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def get_db():
    return sqlite3.connect(DB_PATH)


# ── Routes ───────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "status": "running",
        "project": "Bulbul Bhilala Portfolio API",
        "endpoints": {
            "POST /api/contact": "Submit a contact message",
            "GET  /api/messages": "Retrieve all messages (admin)"
        }
    })


@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    name    = str(data.get("name", "")).strip()
    email   = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "General Enquiry")).strip()
    message = str(data.get("message", "")).strip()

    errors = []
    if not name:
        errors.append("Name is required.")
    if not email or not is_valid_email(email):
        errors.append("A valid email address is required.")
    if not message:
        errors.append("Message cannot be empty.")
    if len(message) > 2000:
        errors.append("Message must be under 2000 characters.")
    if errors:
        return jsonify({"error": " ".join(errors)}), 422

    received = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Save to DB
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO messages (name, email, subject, message, received) VALUES (?,?,?,?,?)",
            (name, email, subject, message, received)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    # Send Gmail notification
    send_gmail(name, email, subject, message)

    print(f"\n📩 New message from {name} <{email}> at {received}")
    print(f"   Subject : {subject}")
    print(f"   Message : {message[:120]}{'...' if len(message) > 120 else ''}\n")

    return jsonify({
        "success": True,
        "message": f"Thanks {name}! Your message has been received."
    }), 201


@app.route("/api/messages", methods=["GET"])
def get_messages():
    token = request.headers.get("X-Admin-Token", "")
    if token != os.environ.get("ADMIN_TOKEN", "bulbul-secret-2026"):
        return jsonify({"error": "Unauthorized. Provide X-Admin-Token header."}), 401

    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM messages ORDER BY received DESC").fetchall()
    conn.close()

    return jsonify({"count": len(rows), "messages": [dict(r) for r in rows]})


@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify({
        "projects": 15,
        "skills": 10,
        "years_experience": 2,
        "happy_clients": 8,
    })


# ── Entry Point ──────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("=" * 50)
    print("  Bulbul Bhilala Portfolio — Flask Backend")
    print("  Running at http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)

