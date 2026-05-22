from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

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

    if not all([name, email, subject, message]):
        return jsonify({"message": "Please fill all fields."}), 400

    if "@" not in email:
        return jsonify({"message": "Please enter a valid email."}), 400

    inbox.append({"name": name, "email": email, "subject": subject, "message": message})
    print(f"[MSG] {name} ({email}): {subject}")

    # Web3Forms handles email — no SMTP needed
    return jsonify({"message": f"Thanks {name}! I'll get back to you soon ✅"})


@app.route("/api/messages")
def get_messages():
    return jsonify(inbox)


# ─── RUN APP ──────────────────────────────────────────

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )