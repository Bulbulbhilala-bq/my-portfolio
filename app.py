from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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
    return jsonify({"message": f"Thanks {name}! I'll get back to you soon ✅"})

@app.route("/api/messages")   # admin peek
def get_messages():
    return jsonify(inbox)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
