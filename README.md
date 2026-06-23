![](<c:/Users/asus vivobook/Documents/prtfl/static/expense.png>)# Bulbul Bhilala — Portfolio

A full-stack personal portfolio with an HTML/CSS/JS frontend and a Python (Flask) backend.

## Project Structure

```
portfolio/
├── index.html        ← Frontend (HTML + CSS + JS)
├── app.py            ← Backend (Python Flask API)
├── requirements.txt  ← Python dependencies
└── README.md
```

---

## Run the Backend

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Flask server

```bash
python app.py
```

Server will run at: `http://localhost:5000`

---

## Open the Frontend

Simply open `index.html` in your browser.

The contact form will POST to `http://localhost:5000/api/contact` automatically.

---

## API Endpoints

| Method | Endpoint        | Description                        |
| ------ | --------------- | ---------------------------------- |
| GET    | `/`             | Health check                       |
| POST   | `/api/contact`  | Submit contact form                |
| GET    | `/api/messages` | View all messages (requires token) |
| GET    | `/api/stats`    | Portfolio stats                    |

### View messages (admin)

```bash
curl -H "X-Admin-Token: bulbul-secret-2026" http://localhost:5000/api/messages
```

Change `ADMIN_TOKEN` in environment variables for production.

---

## Customise

Edit `index.html` to update:

- Your name, bio, skills, and projects (in the JS data arrays at the bottom)
- Social links and email address
- Color theme (CSS variables at the top of `<style>`)

Edit `app.py` to:

- Add email notifications (use `smtplib` or SendGrid)
- Add more API endpoints
- Connect a MySQL/PostgreSQL database instead of SQLite
