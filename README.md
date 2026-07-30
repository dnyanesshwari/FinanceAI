# 💰 FinanceAI – AI-Powered Financial Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react">
  <img src="https://img.shields.io/badge/License-MIT-success?style=for-the-badge">
</p>

<p align="center">
An AI-powered financial assistant that leverages <b>Large Language Models (LLMs)</b>, <b>Retrieval-Augmented Generation (RAG)</b>, and <b>semantic search</b> to answer financial questions using your own documents.
</p>

---

# 🌐 Live Demo

### 🚀 Frontend

**https://agent-6a6b440e3bf81a43--clinquant-kringle-78de32.netlify.app/**

---

# 📖 Overview

FinanceAI is an intelligent financial assistant designed to simplify financial information retrieval.

Instead of relying only on an LLM, FinanceAI uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded financial documents before generating responses.

Users can:

- 💬 Ask financial questions
- 📄 Upload financial documents
- 🔍 Perform semantic search
- 🤖 Get AI-generated responses
- 📚 Build a searchable knowledge base

---

# ✨ Features

## 🤖 AI Financial Assistant

Ask questions in natural language.

Example:

> What is GST?

---

## 📄 Document Upload

Upload PDFs and financial documents.

The documents are indexed into a vector database.

---

## 🔍 Semantic Search

Instead of keyword matching, FinanceAI understands meaning using embeddings.

---

## 🧠 Retrieval-Augmented Generation (RAG)

The system retrieves relevant document chunks before asking the LLM.

This reduces hallucinations and improves answer quality.

---

## 💬 Conversational Chat

Maintain conversation history while interacting with the assistant.

---

## 📚 Knowledge Base

Store and search financial documents efficiently.

---

## ⚡ FastAPI Backend

REST APIs built with FastAPI.

---

## 🎨 Modern Responsive UI

Clean interface built using React.

---

# 🏗️ System Architecture

```
                    User
                      │
                      ▼
              React Frontend
                      │
          REST API Requests
                      │
                      ▼
               FastAPI Backend
                      │
              LangChain Pipeline
                      │
         Retrieval-Augmented Generation
                      │
      ┌───────────────┴───────────────┐
      │                               │
      ▼                               ▼
 Vector Database                 Large Language Model
 (Embeddings)                   (Groq / Gemini)
      │                               │
      └───────────────┬───────────────┘
                      ▼
              AI Generated Response
```

---

# ⚙️ Tech Stack

## Frontend

- React.js
- HTML5
- CSS3
- JavaScript

---

## Backend

- Python
- FastAPI
- LangChain

---

## AI

- Groq LLM
- Google Gemini
- HuggingFace Embeddings

---

## Database

- SQLite

---

## Deployment

- Netlify
- Render / Local Backend

---

# 📂 Project Structure

```
FinanceAI
│
├── Backend
│   ├── app
│   ├── finance_env
│   ├── knowledge_base
│   ├── logs
│   ├── scripts
│   ├── .env
│   ├── requirements.txt
│   └── users.db
│
├── frontend
│
├── README.md
│
└── .gitignore
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/dnyanesshwari/FinanceAI.git

cd FinanceAI
```

---

## Create Virtual Environment

```bash
cd Backend

python -m venv finance_env
```

Activate

### Windows

```bash
finance_env\Scripts\activate
```

### Linux / macOS

```bash
source finance_env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside Backend.

Example:

```env
GROQ_API_KEY=<YOUR_GROQ_API_KEY>

GOOGLE_API_KEY=<YOUR_GEMINI_API_KEY>

SECRET_KEY=your_secret_key
```

---

# ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

or

```bash
python app.py
```

---

# ▶️ Run Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 📸 Screenshots

## 🏠 Home Page

(Add Screenshot)

---

## 💬 Chat Interface

(Add Screenshot)

---

## 📄 Upload Documents

(Add Screenshot)

---

## 📚 Knowledge Base

(Add Screenshot)

---

## 📱 Mobile View

(Add Screenshot)

---

# 💡 Example Questions

```
What is GST?

Explain balance sheet.

Summarize this PDF.

What are startup tax benefits?

Explain income tax slabs.

Difference between assets and liabilities.

What is depreciation?

Generate financial insights from this report.
```

---

# 🔄 Workflow

```
User Question

        │

        ▼

React Frontend

        │

        ▼

FastAPI Backend

        │

        ▼

Generate Embeddings

        │

        ▼

Retrieve Relevant Chunks

        │

        ▼

Send Context to LLM

        │

        ▼

Generate Answer

        │

        ▼

Return Response
```

---

# 📈 Future Improvements

- Voice Assistant
- OCR Support
- Financial Report Analysis
- Portfolio Insights
- Investment Recommendation
- Multilingual Support
- Authentication & User Profiles
- PostgreSQL Integration
- Docker Deployment
- Cloud Deployment
- Admin Dashboard

---

# 📊 Tech Highlights

- ✅ FastAPI REST APIs
- ✅ LangChain Integration
- ✅ Retrieval-Augmented Generation
- ✅ Vector Search
- ✅ LLM Integration
- ✅ React Frontend
- ✅ Financial Document QA
- ✅ Semantic Search

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a new branch

```
git checkout -b feature-name
```

3. Commit changes

```
git commit -m "Added feature"
```

4. Push

```
git push origin feature-name
```

5. Create a Pull Request

---

# 🛡️ License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

## Dnyaneshwari Pawar

🎓 B.Tech CSE (AI & ML)

💼 AI / ML Engineer

🔗 GitHub

https://github.com/dnyanesshwari

---

# ⭐ Support

If you found this project helpful,

⭐ Star the repository

🍴 Fork the project

💬 Share your feedback

---

<p align="center">
Made with ❤️ using Python, FastAPI, LangChain, RAG & Large Language Models
</p>
