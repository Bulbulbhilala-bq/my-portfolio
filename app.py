from flask import Flask, render_template, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Environment variables
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
NOTIFY_TO = os.getenv("NOTIFY_TO")


# ─── EMAIL FUNCTION ───────────────────────────────────

def send_notification(name, email, subject, message):
    try:
        msg = MIMEMultipart("alternative")

        msg["Subject"] = f"📬 New Message from Portfolio: {subject}"
        msg["From"] = YOUR_EMAIL
        msg["To"] = NOTIFY_TO

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding:20px;">
            <h2 style="color:#6c63ff;">📬 New Portfolio Message</h2>

            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>

            <hr>
            <p style="font-size:12px; color:gray;">
                Sent automatically from your portfolio website.
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))

        # ✅ FIXED SMTP CODE
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_EMAIL, YOUR_PASSWORD)
            server.sendmail(
                YOUR_EMAIL,
                NOTIFY_TO,
                msg.as_string()
            )

        print(f"[EMAIL] Notification sent for: {name}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR]: {e}")
        return False


# ─── PROJECTS DATA ───────────────────────────────────

projects_data = [
    {
        "id": 1,
        "tag": "Web App",
        "title": "E-Commerce Platform",
        "description": "Full-stack shopping app with cart, payments & admin dashboard.",
        "tech": ["React", "Flask", "PostgreSQL"],
        "github": "https://github.com",
        "live": "https://example.com"
    },
    {
        "id": 2,
        "tag": "API",
        "title": "REST API Service",
        "description": "Scalable REST API with JWT authentication.",
        "tech": ["Python", "Flask", "Docker"],
        "github": "https://github.com",
        "live": "https://example.com"
    }
]

# Store contact messages temporarily
inbox = []


# ─── ROUTES ───────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(projects_data)


@app.route("/api/projects/<int:pid>", methods=["GET"])
def get_project(pid):
    p = next((x for x in projects_data if x["id"] == pid), None)

    if p:
        return jsonify(p)

    return jsonify({"error": "Not found"}), 404


@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    # Validation
    if not all([name, email, subject, message]):
        return jsonify({
            "message": "Please fill all fields."
        }), 400

    if "@" not in email:
        return jsonify({
            "message": "Please enter a valid email."
        }), 400

    # Save message
    inbox.append({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    })

    print(f"[MSG] {name} ({email}): {subject}")

    # Send email notification
    send_notification(name, email, subject, message)

    return jsonify({
        "message": f"Thanks {name}! I'll get back to you soon ✅"
    })


@app.route("/api/messages")
def get_messages():
    return jsonify(inbox)


# ─── RUN APP ──────────────────────────────────────────

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )