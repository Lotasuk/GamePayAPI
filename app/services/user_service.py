from typing import List, Sequence
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.models import User
from app.database.repo.user_repository import UserRepository
from app.utils.result import Result, err, success
from app.schems.request.access import AccessRequest
from app.security.hasher import hash_password

class UserService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: UserRepository = UserRepository(session)

    async def delete_account(self, userId: str):
        return await self._repo.delete_by_id(userId)

    async def get_by_email(self, email: str):
        user = await self._repo.get_by_email(email)
        return success(user) if user else err("Пользователь не найден.")

    async def register(self, register_request: AccessRequest) -> Result[None]:
        try:
            inserted = await self._repo.create(Email=register_request.email, PasswordHash=hash_password(register_request.password))
            await self._repo.commit()
        except IntegrityError as e:
            return err(str(e))
        return success("Пользователь успешно зарегистрирован.")

    async def auth(self, request: AccessRequest) -> Result[str]:
        authenticated = await self._repo.authenticate_user(request.email, request.password)
        if not authenticated.success:
            return err("Неправильный логин или пароль")
        return success(authenticated.value.UserID)
