# 💰 Finance AI

An intelligent financial assistant powered by FastAPI and RAG (Retrieval-Augmented Generation). Ask finance questions in natural language, use built-in calculators, and track your conversation history — all behind secure JWT authentication.

---

## 🗂 Project Structure

```
fastapi_backend/
├── app/
│   ├── auth/
│   │   ├── auth_utils.py        # JWT creation, hashing, token decode
│   │   └── user_store.py        # User persistence (SQLite)
│   ├── services/
│   │   ├── query_service.py     # RAG-based answer generation
│   │   ├── intent_service.py    # Query intent classification
│   │   ├── memory_service.py    # Per-user conversation memory
│   │   └── finance_tools.py     # EMI, SI, CI calculators
│   └── utils/
│       └── logger.py            # Logging setup
├── frontend/
│   ├── index.html               # Full-screen chat UI
│   └── config.js                # Backend URL config
├── knowledge_base/              # Documents for RAG retrieval
├── finance_index/               # Vector index storage
├── logs/                        # Application logs
├── scripts/                     # Utility/setup scripts
├── .env                         # Environment variables
├── requirements.txt
├── users.db                     # SQLite user database
└── main.py                      # FastAPI entry point
```

---

## ✨ Features

- 🤖 **AI Chat** — Ask any finance question; answers are generated using RAG over your knowledge base
- 🔐 **Auth** — Secure signup/login with JWT tokens; all routes are protected
- 📊 **EMI Calculator** — Calculate equated monthly instalments
- 💰 **Simple Interest** — Quick SI computation
- 📈 **Compound Interest** — CI with annual compounding
- 🕘 **Chat History** — View and clear your past conversations per session
- 🌙 **Dark / Light Mode** — Theme toggle that persists across sessions
- 🚦 **Rate Limiting** — Slowapi-based rate limiting per IP

---

## ⚙️ Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd fastapi_backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root:

```env
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Open your browser at **http://localhost:8000** — the frontend is served automatically.

---

## 🔌 API Reference

All routes except `/login` and `/signup` require a Bearer token in the `Authorization` header.

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/signup?username=x&password=y` | Create a new account |
| `POST` | `/login` | Login (form-encoded); returns JWT token |

### Chat

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `POST` | `/ask` | `{ "query": "string" }` | Ask a finance question |
| `GET`  | `/history` | — | Get current user's chat history |
| `POST` | `/clear-session` | — | Clear current user's chat history |

### Finance Tools

All tool endpoints accept: `{ "principal": float, "rate": float, "time": float }`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tools/emi` | EMI calculator |
| `POST` | `/tools/simple-interest` | Simple interest |
| `POST` | `/tools/compound-interest` | Compound interest |

### Example: Login then Ask

```bash
# 1. Login
curl -X POST http://localhost:8000/login \
  -d "username=alice&password=secret123"

# 2. Use the token
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is dollar cost averaging?"}'
```

---

## 🖥 Frontend

The frontend is a single `index.html` file served statically by FastAPI. No build step required.

**Configuration** — edit `frontend/config.js`:

```js
// Leave empty when served by FastAPI (same origin)
const API_BASE_URL = "";

// Use this only for local dev with a separate frontend server
// const API_BASE_URL = "http://localhost:8000";
```

**Features:**
- Full-screen responsive layout with sidebar
- Login / Signup modals
- Quick-action buttons (Budgeting Tips, Market Trends, etc.)
- Tool modals with live results from backend
- Chat history viewer with clear option
- Dark / Light theme toggle (persists via localStorage)
- JWT stored in localStorage; auto-logout on token expiry

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| AI / RAG | LangChain / custom RAG pipeline |
| Auth | JWT (python-jose) + bcrypt |
| Database | SQLite (users.db) |
| Rate Limiting | Slowapi |
| Frontend | Vanilla HTML, CSS, JS |
| Vector Store | Local index (finance_index/) |

---

## 📝 Notes

- The `/clear-session` endpoint clears memory for the **currently logged-in user** — no session ID needed, it's derived from the JWT token.
- Intent classification runs on every `/ask` request and is returned in the response alongside `response_time`.
- The knowledge base lives in `knowledge_base/` — add `.pdf` or `.txt` files there and re-index to expand the AI's financial knowledge.

---

## 📄 License

MIT
