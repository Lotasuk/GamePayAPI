from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repo.chat_repo import ChatRepository
from app.database.models.models import Chat, Message

class ChatService:
    def __init__(self, session: AsyncSession):
        self._repo = ChatRepository(session)

    async def start_chat(self, user1_id: int, user2_id: int) -> Chat:
        # Проверяем, существует ли уже чат
        chat = await self._repo.get_chat_by_users(user1_id, user2_id)
        if not chat:
            chat = await self._repo.create_chat(user1_id, user2_id)
        return chat

    async def send_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        return await self._repo.send_message(chat_id, sender_id, content)

    async def get_chat_history(self, chat_id: int, limit: int = 100) -> List[Message]:
        return await self._repo.get_messages(chat_id, limit)

    async def mark_message_as_read(self, message_id: int):
        await self._repo.mark_as_read(message_id)