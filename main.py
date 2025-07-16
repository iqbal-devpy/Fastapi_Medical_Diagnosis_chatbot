from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response
import os
from chatbot import handle_chat
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
# from authlib.integrations.starlette_client import StarletteRemoteApp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import User, Chat
from database import get_async_session
import logging
import secrets
import bleach
from datetime import datetime
import mysql.connector
from passlib.context import CryptContext

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure logging
log_dir = "D:\Programming Codes\python test codes\MYPROJECTS\chatbot\Fastapi_med_bot\logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")
handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.info("Server startup - Attempting to log to %s", log_file)
with open(log_file, 'a') as f:
    f.write("Test write to confirm file access\n")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER", "your_username"),
    password=os.getenv("MYSQL_PASSWORD", "your_password"),
    database=os.getenv("MYSQL_DATABASE", "your_database")
)


# Dependency to get current user from session
async def get_current_user(request: Request):
    user = request.session.get("user")
    return user if user else {"username": "Guest", "id": 0}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(get_async_session), user: dict = Depends(get_current_user)):
    try:
        current_user = user
        result = await db.execute(
            select(Chat).where(Chat.user_id == current_user["id"], Chat.is_deleted == False).order_by(Chat.timestamp)
        )
        chats = result.scalars().all()
        chat_history = []
        for chat in chats:
            chat_history.append({
                "user": True,
                "text": chat.message,
                "timestamp": chat.timestamp
            })
            chat_history.append({
                "user": False,
                "text": bleach.clean(chat.response, tags=['p', 'ul', 'li', 'h3', 'strong'], attributes={}),
                "timestamp": chat.timestamp
            })
        dark_mode = request.session.get("dark_mode", False)
        logger.info(f"Root accessed by user: {current_user['username']}, History: {len(chat_history)} messages")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "user": current_user, "chat_history": chat_history, "dark_mode": dark_mode}
        )
    except Exception as e:
        logger.error(f"Error in root: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/chat")
async def chat(request: Request, message: str = Form(...), db: AsyncSession = Depends(get_async_session), user: dict = Depends(get_current_user)):
    try:
        user_message = message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Empty message")
        current_user = user
        bot_response = await handle_chat(current_user["id"], user_message, db)
        if not bot_response:
            bot_response = "Sorry, I couldn't process your request."
        bot_response = bleach.clean(bot_response, tags=['p', 'ul', 'li', 'h3', 'strong'], attributes={})
        chat = Chat(user_id=current_user["id"], message=user_message, response=bot_response, timestamp=datetime.now())
        db.add(chat)
        try:
            await db.commit()
        except IntegrityError as ie:
            logger.error(f"Integrity error in chat: {str(ie)}")
            await db.rollback()
            raise HTTPException(status_code=400, detail="Invalid user ID, please log in or register.")
        logger.info(f"Chat processed: User: {user_message}, Bot: {bot_response}")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        await db.rollback()
        bot_response = "Sorry, an error occurred. Please try again."
        bot_response = bleach.clean(bot_response, tags=['p', 'ul', 'li', 'h3', 'strong'], attributes={})
        chat = Chat(user_id=current_user["id"], message=user_message, response=bot_response, timestamp=datetime.now())
        try:
            db.add(chat)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to log error message.")
    return RedirectResponse(url="/", status_code=303)

@app.post("/clear_chat")
async def clear_chat(request: Request, db: AsyncSession = Depends(get_async_session), user: dict = Depends(get_current_user)):
    try:
        current_user = user
        await db.execute(
            Chat.__table__.update()
            .where(Chat.user_id == current_user["id"], Chat.is_deleted == False)
            .values(is_deleted=True)
        )
        await db.commit()
        logger.info("Chat history marked as cleared")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        logger.error(f"Error in clear_chat: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_async_session), user: dict = Depends(get_current_user)):
    try:
        current_user = user
        result = await db.execute(
            select(Chat).where(Chat.user_id == current_user["id"], Chat.is_deleted == False).order_by(Chat.timestamp)
        )
        chats = result.scalars().all()
        for chat in chats:
            chat.response = bleach.clean(chat.response, tags=['p', 'ul', 'li', 'h3', 'strong'], attributes={})
        dark_mode = request.session.get("dark_mode", False)
        logger.info(f"Dashboard accessed by user: {current_user['username']}")
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "user": current_user, "chat_history": chats, "dark_mode": dark_mode}
        )
    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/toggle_dark_mode")
async def toggle_dark_mode(request: Request):
    try:
        request.session["dark_mode"] = not request.session.get("dark_mode", False)
        logger.info(f"Dark mode toggled to: {request.session['dark_mode']}")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        logger.error(f"Error in toggle_dark_mode: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle dark mode")
