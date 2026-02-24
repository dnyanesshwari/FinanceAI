# 💰 FINANCE AI – Intelligent Financial Assistant

FINANCE AI is a full-stack AI-powered financial assistant built using **FastAPI (backend)** and **React + Tailwind CSS (frontend)**.

It provides secure authentication, AI-powered financial chat, financial calculators (EMI, Simple Interest, Compound Interest), and user-specific chat history.

---

## 🚀 Features

- 🔐 JWT-based Authentication (Signup / Login)
- 💬 AI Financial Chat Assistant
- 🧠 User-based Conversation Memory
- 📊 EMI Calculator
- 💵 Simple Interest Calculator
- 📈 Compound Interest Calculator
- 📜 Chat History API
- 🎨 Modern UI with Tailwind CSS
- ⚡ FastAPI backend with modular architecture
- 🌐 CORS enabled for frontend-backend communication

---

## 🏗 Project Architecture
finance-project/
│
├── backend/
│ ├── app/
│ │ ├── auth/
│ │ ├── services/
│ │ ├── rag/
│ │ ├── utils/
│ │ └── db/
│ │
│ ├── main.py
│ ├── requirements.txt
│ ├── .env
│ └── users.db
│
└── frontend/
├── src/
├── index.html

---

# ⚙️ Backend Setup (FastAPI)

2️⃣ Create Virtual Environment
python -m venv venv
Activate Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Backend Server
uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000

Swagger API Docs:

http://127.0.0.1:8000/docs

🔐 Authentication Flow

POST /signup → Create account

POST /login → Receive JWT token

Token stored in browser (localStorage)

Protected endpoints require:

Authorization: Bearer <token>


🛠 API Endpoints
💬 Chat Assistant
POST /ask

Request:

{
  "query": "How should I invest ₹30,000 salary?"
}
📊 EMI Calculator
POST /tools/emi

Request:

{
  "principal": 100000,
  "rate": 8.5,
  "time": 2
}
💵 Simple Interest
POST /tools/simple-interest

Request:

{
  "principal": 100000,
  "rate": 6.5,
  "time": 5
}
📈 Compound Interest
POST /tools/compound-interest

Request:

{
  "principal": 100000,
  "rate": 6.5,
  "time": 5
}
🧠 Get User Chat History
GET /history

