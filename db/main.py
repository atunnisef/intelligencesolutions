from fastapi import FastAPI, HTTPException
from database import database, metadata, engine
from models import users, chat_messages
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Create tables
metadata.create_all(engine)

class MessageIn(BaseModel):
    user_id: str
    role: str
    message: str

class MessageOut(MessageIn):
    timestamp: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", status_code=201)
async def create_user(user_id: str, name: str = None):
    query = users.insert().values(id=user_id, name=name)
    try:
        await database.execute(query)
    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"id": user_id, "name": name}

@app.post("/messages/", status_code=201, response_model=MessageOut)
async def add_message(message: MessageIn):
    # Ensure user exists
    user = await database.fetch_one(users.select().where(users.c.id == message.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = chat_messages.insert().values(
        user_id=message.user_id,
        role=message.role,
        message=message.message,
    )
    last_record_id = await database.execute(query)

    # Return inserted message (fetch timestamp)
    db_message = await database.fetch_one(chat_messages.select().where(chat_messages.c.id == last_record_id))
    return db_message

@app.get("/messages/{user_id}", response_model=List[MessageOut])
async def get_messages(user_id: str):
    query = chat_messages.select().where(chat_messages.c.user_id == user_id).order_by(chat_messages.c.timestamp)
    rows = await database.fetch_all(query)
    return rows
