# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.llm_engine import init_chain, ask_with_history

app = FastAPI(title="Astrobot Chatbot")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chat_history = []

@app.on_event("startup")
def init():
    init_chain()

@app.get("/", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    global chat_history
    response = ask_with_history(req.message, chat_history)
    chat_history.append((req.message, response))
    return { "response": response }

