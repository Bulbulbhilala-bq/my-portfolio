from flask import Flask, render_template, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)


YOUR_EMAIL    = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
NOTIFY_TO     = os.getenv("NOTIFY_TO")       # <-- jahan notification aaye (same ya alag)

def send_notification(name, email, subject, message):
    """Naya message aane pe email notification bhejo"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📬 New Message from Portfolio: {subject}"
        msg["From"]    = YOUR_EMAIL
        msg["To"]      = NOTIFY_TO

        html_body = f"""
        <html><body style="font-family:Arial,sans-serif; max-width:600px; margin:auto; padding:20px;">
          <h2 style="color:#6c63ff; border-bottom:2px solid #6c63ff; padding-bottom:10px;">
            📬 New Portfolio Message
          </h2>
          <table style="width:100%; border-collapse:collapse;">
            <tr><td style="padding:8px; font-weight:bold; color:#555;">Name:</td>
                <td style="padding:8px;">{name}</td></tr>
            <tr style="background:#f9f9f9;">
                <td style="padding:8px; font-weight:bold; color:#555;">Email:</td>
                <td style="padding:8px;"><a href="mailto:{email}">{email}</a></td></tr>
            <tr><td style="padding:8px; font-weight:bold; color:#555;">Subject:</td>
                <td style="padding:8px;">{subject}</td></tr>
            <tr style="background:#f9f9f9;">
                <td style="padding:8px; font-weight:bold; color:#555; vertical-align:top;">Message:</td>
                <td style="padding:8px;">{message}</td></tr>
          </table>
          <p style="color:#888; font-size:12px; margin-top:20px;">
            Yeh email aapke portfolio se automatic bheji gayi hai.
          </p>
        </body></html>
        """

        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
         server.starttls()
         server.login(YOUR_EMAIL, YOUR_PASSWORD)
         server.sendmail(YOUR_EMAIL, NOTIFY_TO, msg.as_string())


        print(f"[EMAIL] Notification sent for: {name} ({email})")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ─── PROJECTS DATA ─────────────────────────────────────
projects_data = [
    {
        "id": 1, "tag": "Web App",
        "title": "E-Commerce Platform",
        "description": "Full-stack shopping app with cart, payments & admin dashboard built with React + Flask.",
        "tech": ["React", "Flask", "PostgreSQL", "Stripe"],
        "github": "https://github.com", "live": "https://example.com"
    },
    {
        "id": 2, "tag": "API",
        "title": "REST API Service",
        "description": "Scalable REST API with JWT authentication, rate limiting, and full Swagger documentation.",
        "tech": ["Python", "Flask", "Redis", "Docker"],
        "github": "https://github.com", "live": "https://example.com"
    },
    {
        "id": 3, "tag": "Dashboard",
        "title": "Analytics Dashboard",
        "description": "Real-time analytics dashboard with interactive charts, filters, and CSV export.",
        "tech": ["JavaScript", "Chart.js", "Flask", "SQLite"],
        "github": "https://github.com", "live": "https://example.com"
    },
    {
        "id": 4, "tag": "ML App",
        "title": "AI Chat Assistant",
        "description": "Intelligent chatbot powered by NLP with conversation history and context awareness.",
        "tech": ["Python", "Flask", "OpenAI", "MongoDB"],
        "github": "https://github.com", "live": "https://example.com"
    }
]

inbox = []   # in-memory contact messages

# ─── ROUTES ────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(projects_data)

@app.route("/api/projects/<int:pid>", methods=["GET"])
def get_project(pid):
    p = next((x for x in projects_data if x["id"] == pid), None)
    return jsonify(p) if p else (jsonify({"error": "Not found"}), 404)

@app.route("/api/contact", methods=["POST"])
def contact():
    data    = request.get_json()
    name    = data.get("name",    "").strip()
    email   = data.get("email",   "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, subject, message]):
        return jsonify({"message": "Please fill all fields."}), 400
    if "@" not in email:
        return jsonify({"message": "Please enter a valid email."}), 400

    inbox.append({"name": name, "email": email,
                  "subject": subject, "message": message})
    print(f"[MSG] {name} ({email}): {subject}")

    # ✅ Email notification bhejo
    send_notification(name, email, subject, message)

    return jsonify({"message": f"Thanks {name}! I'll get back to you soon ✅"})

@app.route("/api/messages")   # admin peek
def get_messages():
    return jsonify(inbox)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
