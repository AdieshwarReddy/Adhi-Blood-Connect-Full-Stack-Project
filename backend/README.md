# Adhi Blood Connect - FastAPI Backend

Production-ready, async-first clean architecture backend for the **Adhi Blood Connect** platform. Built using **FastAPI**, **MongoDB Atlas**, **WebSockets**, and **Gemini API**.

---

## 🛠️ Architecture & Folder Structure

This backend is designed with a **Clean Architecture** approach to isolate concerns, maintain decoupling, and ensure testability:

```text
/backend
├── app/
│   ├── api/                   # API Endpoints (V1 Controllers)
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── emergency.py
│   │       ├── notifications.py
│   │       ├── chatbot.py
│   │       └── websocket_routes.py
│   ├── core/                  # Configuration, Database Initialization & Security Settings
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── logger.py
│   ├── models/                # Database Document Models
│   ├── schemas/               # Pydantic Input/Output Validation Schemas
│   ├── services/              # Pure Business Logic (Matching Engine, AI Chat, etc.)
│   ├── middleware/            # Rate limiting, Auth & Logging middleware
│   ├── utils/                 # Validators, Helpers, Blood Compatibility Matrix
│   ├── websocket/             # WebSocket connection management
│   ├── background/            # Background tasks (Email/SMS placeholders)
│   └── main.py                # FastAPI Application Entrypoint & Lifespan Hooks
├── requirements.txt           # Python Project Dependencies
├── Dockerfile                 # Multi-stage optimized Docker packaging
├── docker-compose.yml         # Local Docker Orchestration
├── .env.example               # Environment Configuration Blueprint
└── README.md                  # This documentation
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.12+
* MongoDB Atlas cluster or local MongoDB instance
* (Optional) Redis server for rate-limiting

### Local Manual Setup

1. **Clone & Navigate** to the backend directory:
   ```bash
   cd backend
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment**:
   Copy `.env.example` to `.env` and fill in your connection details (such as `MONGODB_URL` and `GEMINI_API_KEY`):
   ```bash
   cp .env.example .env
   ```

5. **Run the Development Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. Open **Swagger Docs** at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker Deployment

To spin up the entire backend stack (FastAPI, MongoDB, Redis) instantly:

```bash
docker-compose up --build
```

---

## 🔑 Core Features

### 1. Smart Donor Matching Algorithm
The matching engine ranks donors based on a combination of:
* **Blood Group Compatibility**: Detailed matrix lookup.
* **Geospatial Distance**: Native MongoDB `2dsphere` query ($near) + Haversine calculation.
* **Availability & Cool-down**: Excluding donors who are marked unavailable or have donated in the last 90 days.
* **Reliability Score**: Weighted rating based on donation history.

### 2. Real-time Notifications & WebSockets
Maintains a stateful active registry mapping active User IDs to active WebSocket channels. Handles broadcasts for emergency events instantly.

### 3. AI Medical Chatbot
Integrates with the **Gemini API** (`gemini-1.5-flash`) for medical FAQs, blood donation eligibility checklists, and post-donation care tips, with rigorous prompt validation.
