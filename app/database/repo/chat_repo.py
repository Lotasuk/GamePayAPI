from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from app.database.models.models import Chat, Message

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_chat(self, user1_id: int, user2_id: int) -> Chat:
        chat = Chat(User1ID=user1_id, User2ID=user2_id)
        self._session.add(chat)
        await self._session.commit()
        return chat

    async def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[Chat]:
        result = await self._session.execute(
            select(Chat).where(
                and_(
                    Chat.User1ID == user1_id,
                    Chat.User2ID == user2_id
                )
            )
        )
        return result.scalars().first()

    async def send_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        message = Message(ChatID=chat_id, SenderID=sender_id, Content=content)
        self._session.add(message)
        await self._session.commit()
        return message

    async def get_messages(self, chat_id: int, limit: int = 100) -> List[Message]:
        result = await self._session.execute(
            select(Message)
            .where(Message.ChatID == chat_id)
            .order_by(Message.SentAt.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def mark_as_read(self, message_id: int):
        await self._session.execute(
            update(Message)
            .where(Message.MessageID == message_id)
            .values(IsRead=True)
        )
        await self._session.commit()