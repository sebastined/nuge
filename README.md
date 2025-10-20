# 🌀 Nuge App

**Nuge** is a simple yet powerful Flask web application that provides both a **web UI** and a **REST API** for generating random numbers within a configurable range.  

It’s designed as a lightweight example of a Python microservice suitable for containerization and Kubernetes deployment using Jenkins and Kaniko.

---

## 🚀 Features

- **Flask Backend:** Serves REST endpoints for random number generation.
- **Static Frontend:** Clean, responsive HTML UI with dark mode toggle.
- **API + UI:** Access results via `/api/random` or `/`.
- **Lightweight:** Single Python file + static assets.
- **Ready for CI/CD:** Jenkinsfile included with Kaniko build and K8s deployment.

---

## ⚙️ How It Works

The app serves an HTML interface (`/static/index.html`) and exposes two API endpoints:

| Method | Endpoint | Description | Example |
|--------|-----------|-------------|----------|
| GET | `/api/random` | Generates random numbers using query parameters | `/api/random?min=1&max=10&count=5` |
| POST | `/api/random` | Accepts JSON body and returns random numbers | `{"min": 0, "max": 100, "count": 10}` |

Example API response:
```json
[17, 56, 93, 14, 78]
