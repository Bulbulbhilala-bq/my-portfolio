from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# ─── PROJECTS DATA ───────────────────────────────────
projects_data = [
    {
        
    "id": 1,
    "tag": "Web App",
    "title": "Oak Haven Furniture E-Commerce UI",
    "description": "Oak Haven Furniture E-Commerce UI",
    "tech": ["Figma","UI/UX Design","HTML","CSS","JavaScript"],
    "github": "https://github.com",
    "live": "https://example.com",
    "image": "/static/ecoomerse.png"
 },
    {
        "id": 2,
        "tag": "Frontend",
        "title": " Zafran — Fine Dining Restaurant Website",
        "description": " A fully responsive restaurant website with interactive menu filters, table reservation form & elegant dark UI..",
        "tech": ["HTML", "CSS", "JavaScript","Responsive Design"],
        "github": "https://github.com",
        "live": "https://zafran-frontend.netlify.app",
         "image": "static/{A8B3F12F-03D4-4709-9C38-50A4447BBE1A}.png"
        
    },
    {
        "id": 3,
        "tag": "App Design",
        "title": "Food Delivery App Design",
        "description": "Modern food delivery mobile app UI designed in Figma with clean layouts, interactive product screens, and user-friendly navigation.",
        "tech": ["Figma","UI/UX Design","Mobile App Design","Prototype Design"],
        "github": "https://github.com",
        "live": "https://example.com",
         "image": "static/{86BA08E1-03FD-4687-B44A-5996D87DCEF7}.png"
    },
    {
        "id": 4,
        "tag": "Modern UI/UX Portfolio Website",
        "title": "E-Commerce UI",
        "description": "Modern UI/UX portfolio website with responsive and creative design.",
        "tech": ["Figma","HTML","CSS","JavaScript","UI/UX Design"],
        "github": "https://github.com",
        "live": "https://example.com",
         "image": "static/{6ACFF61D-F593-4BDC-BC89-2922DA30D7FA}.png"
    },
       {
    "id": 5,
    "tag": "Mobile App UI",
    "title": "Coffee Ordering App UI",
    "description": "Modern coffee ordering mobile app UI with onboarding, product details, cart, and checkout screens designed in Figma.",
    "tech": ["Figma", "UI/UX Design", "Mobile App Design"],
    "github": "https://github.com",
    "live": "https://example.com",
    "image": "/static/{A3BE337E-63E9-4FC2-9CE7-4D26702DC63C}.png"

    },
    {
    "id": 6,
    "tag": "Expense Tracker Web App",
    "title": "Expense Management Dashboard",
    "description": "A modern expense tracking dashboard to manage daily expenses, categorize spending, monitor transactions, and analyze financial records with a clean and responsive UI.",
    "tech": ["HTML", "CSS", "JavaScript", "Flask", "Python"],
    "github": "https://github.com",
    "live": "https://example.com",
    "image": "static/{4B863567-0070-4484-9F18-6B974236C07F}.png"
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