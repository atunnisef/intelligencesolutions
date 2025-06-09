from sqlalchemy import Table, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True, index=True),
    Column("name", String, nullable=True),
)

chat_messages = Table(
    "chat_messages",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", String, ForeignKey("users.id")),
    Column("role", String),  # 'user' or 'assistant'
    Column("message", Text),
    Column("timestamp", DateTime(timezone=True), server_default=func.now()),
)
