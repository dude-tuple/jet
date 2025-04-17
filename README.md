# 🛰️ GitHub Webhook App

A FastAPI-based GitHub webhook listener that receives issue events from GitHub and stores them in a PostgreSQL.

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone git@github.com:dude-tuple/jet.git
cd jet
```

### 2. Start the stack with Docker

```bash
docker compose up -d
```

### 3. Run database migrations

```bash
docker exec github_webhook_app alembic upgrade head
```

### 4. Run the app (manually or via PyCharm)

```bash
docker exec github_webhook_app /usr/local/bin/python3 /app/main.py
```

Or use **Run/Debug Configuration** in **PyCharm** to launch the app.


![image](https://github.com/user-attachments/assets/f4ac1128-f321-4156-831c-684d3ec57a22)

---

## 🛠️ Tech Stack

- **FastAPI** — Web server
- **SQLAlchemy** — ORM
- **Pydantic** - validation
- **Alembic** — Migrations
- **PostgreSQL** — Database
- **Docker Compose** — Local development
- **GitHub Webhooks** — Payload source

---

## Docs 
Swagger docs are available at 0.0.0.0:8000/docs
![image](https://github.com/user-attachments/assets/8756973a-9ef7-4c7e-a80e-60c0ce806a81)

## 📦 Environment

Make sure the following environment variable is set (Docker Compose handles this automatically):

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/webhookdb
```

---

## ✅ TODO

- [ ] Validate GitHub HMAC signature
- [ ] Add rate limiting to the webhook endpoint
- [ ] Improve logging and monitoring 
- [ ] Add unit and integration tests
- [ ] Implement /health endpoint
- [ ] Handle additional GitHub events (e.g. PRs, comments)

      
