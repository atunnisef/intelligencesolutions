from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import Dict, List
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_with_memory(msg: Message):
    user_id = msg.user_id

    # Get or create history for user
    if user_id not in user_sessions:
        user_sessions[user_id] = [{"role": "system", "content": "You are a friendly AI support assistant."}]
    
    # Append user message
    user_sessions[user_id].append({"role": "user", "content": msg.message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=user_sessions[user_id]
        )

        assistant_message = response.choices[0].message.content

        # Add assistant response to memory
        user_sessions[user_id].append({"role": "assistant", "content": assistant_message})

        return {
            "response": assistant_message,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        }

    except Exception as e:
        return {"error": str(e)}

# @app.post("/chat")
# async def chat_with_ai(msg: Message):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a friendly customer service assistant for a retail business. Be concise, helpful, and accurate."},
#                 {"role": "user", "content": msg.message}
#             ]
#         )
#         return {"response": response.choices[0].message["content"]}
#     except Exception as e:
#         return {"error": str(e)}
