from pydantic import BaseModel
from datetime import datetime

class ChatCreate(BaseModel):
    user1_id: int
    user2_id: int

class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    content: str

class MessageResponse(BaseModel):
    message_id: int
    chat_id: int
    sender_id: int
    content: str
    sent_at: datetime
    is_read: bool