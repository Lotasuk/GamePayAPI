from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connector import get_session
from app.database.models.models import Chat
from app.services.chat_service import ChatService
from app.schems.chat import ChatCreate, MessageCreate, MessageResponse
from fastapi import WebSocket

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/start", response_model=Chat)
async def start_chat(
    chat_data: ChatCreate,
    session: AsyncSession = Depends(get_session)
):
    service = ChatService(session)
    chat = await service.start_chat(chat_data.user1_id, chat_data.user2_id)
    return chat

@chat_router.websocket("/ws/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Обработка сообщения и рассылка участникам чата
        await websocket.send_text(f"Message received: {data}")

@chat_router.post("/send", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    session: AsyncSession = Depends(get_session)
):
    service = ChatService(session)
    message = await service.send_message(
        message_data.chat_id,
        message_data.sender_id,
        message_data.content
    )
    return message

@chat_router.get("/history/{chat_id}", response_model=List[MessageResponse])
async def get_chat_history(
    chat_id: int,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    service = ChatService(session)
    messages = await service.get_chat_history(chat_id, limit)
    return messages

@chat_router.post("/read/{message_id}")
async def mark_message_as_read(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = ChatService(session)
    await service.mark_message_as_read(message_id)
    return {"status": "Message marked as read"}