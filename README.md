# FinanceAI

A FastAPI financial-assistance chatbot with Groq-powered answers, authentication, financial calculators, conversation history, and a local finance-document knowledge base.

## Run locally

```powershell
cd Backend
.\finance_env\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Add your GROQ_API_KEY to .env
.\finance_env\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://localhost:8000.

## Notes

- The chat uses Groq. Set `GROQ_API_KEY` in `Backend/.env`; do not commit that file.
- RAG uses the checked-in FAISS index. If the embedding model is not cached, chat still works without document retrieval until the model can be downloaded.
- `Backend/users.db` and `Backend/logs/` are local runtime data and are intentionally excluded from version control.
