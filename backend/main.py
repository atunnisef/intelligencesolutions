from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
from database import database
from models import users, chat_messages
from sqlalchemy import select

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_id: str
    message: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/chat")
async def chat_with_memory(msg: Message):
    # Check user exists or create
    user = await database.fetch_one(users.select().where(users.c.id == msg.user_id))
    if not user:
        # Create user record if missing
        await database.execute(users.insert().values(id=msg.user_id, name=None))

    # Load last 10 chat messages for this user (chronological order)
    query = (
        select(chat_messages)
        .where(chat_messages.c.user_id == msg.user_id)
        .order_by(chat_messages.c.timestamp.desc())
        .limit(10)
    )
    rows = await database.fetch_all(query)
    history = [{"role": row["role"], "content": row["message"]} for row in reversed(rows)]

    # Start with system prompt
    messages = [{"role": "system", "content": "You are a friendly AI support assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": msg.message})

    # Call OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        assistant_message = response.choices[0].message.content

        # Save user message
        await database.execute(chat_messages.insert().values(
            user_id=msg.user_id,
            role="user",
            message=msg.message,
            timestamp=datetime.utcnow(),
        ))

        # Save assistant message
        await database.execute(chat_messages.insert().values(
            user_id=msg.user_id,
            role="assistant",
            message=assistant_message,
            timestamp=datetime.utcnow(),
        ))

        return {
            "response": assistant_message,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": msg.user_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
