import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.services.query_service import generate_answer
from app.services.intent_service import classify_intent
from app.services.memory_service import add_to_memory
from app.utils.logger import logger

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.auth_utils import hash_password, verify_password, create_access_token, decode_token
from app.auth.user_store import add_user, get_user

from slowapi import Limiter
from slowapi.util import get_remote_address


from app.services.finance_tools import (
    calculate_emi,
    calculate_simple_interest,
    calculate_compound_interest
)

from app.services.memory_service import get_memory


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
class QueryRequest(BaseModel):
    query: str

class FinanceRequest(BaseModel):
    principal: float
    rate: float
    time: float


@app.post("/ask")
def ask(request: QueryRequest, current_user: str = Depends(get_current_user)):

    start_time = time.time()

    try:
        logger.info(f"Query received: {request.query}")

        intent = classify_intent(request.query)
        answer = generate_answer(request.query, current_user)



        add_to_memory(current_user, request.query, answer)



        response_time = round(time.time() - start_time, 2)
        logger.info(f"Intent: {intent} | Time: {response_time}s")

        return {
            "query": request.query,
            "intent": intent,
            "response": answer,
            "response_time": response_time
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "error": "Something went wrong",
            "details": str(e)
        }
@app.post("/clear-session")
def clear_session(session_id: str):
    from app.services.memory_service import clear_session_memory
    clear_session_memory(session_id)
    return {"message": "Session cleared"}
@app.post("/signup")
def signup(username: str, password: str):
    if get_user(username):
        raise HTTPException(
            status_code=400,
            detail="Account already exists. Please login."
        )

    hashed = hash_password(password)
    add_user(username, hashed)

    return {
        "message": "Account created successfully. Please login to continue."
    }
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please create an account using /signup."
        )

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password. Please try again."
        )

    access_token = create_access_token({
        "sub": form_data.username,
        "role": user["role"]
    })


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")   # opening the app in browser

@app.post("/tools/emi")
def emi_tool(data: FinanceRequest, current_user: str = Depends(get_current_user)):

    result = calculate_emi(data.principal, data.rate, data.time)

    answer = f"Your EMI is ₹{result}"

    add_to_memory(current_user, "EMI Calculation", answer)

    return {
        "tool": "EMI Calculator",
        "emi": result
    }


@app.post("/tools/simple-interest")
def simple_interest_tool(data: FinanceRequest, current_user: str = Depends(get_current_user)):

    result = calculate_simple_interest(data.principal, data.rate, data.time)

    answer = f"Simple interest is ₹{result}"

    add_to_memory(current_user, "Simple Interest Calculation", answer)

    return {
        "tool": "Simple Interest",
        "interest": result
    }


@app.post("/tools/compound-interest")
def compound_interest_tool(data: FinanceRequest, current_user: str = Depends(get_current_user)):

    result = calculate_compound_interest(data.principal, data.rate, data.time)

    answer = f"Compound interest is ₹{result}"

    add_to_memory(current_user, "Compound Interest Calculation", answer)

    return {
        "tool": "Compound Interest",
        "interest": result
    }


from app.services.memory_service import get_user_history

@app.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    history = get_user_history(current_user)
    return {
        "username": current_user,
        "history": history
    }


app.mount("/", StaticFiles(directory="frontend"), name="frontend")  # serves config.js etc.