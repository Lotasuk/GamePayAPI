from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.security.hasher import verify_password
from app.database.models.models import User
from app.database.abstract.abc_repo import AbstractRepository
from sqlalchemy import delete, select, update, insert
from app.utils.result import Result, err, success

class UserRepository(AbstractRepository):
    model = User

    async def create(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def update_by_id(self, userId: str, **kwargs):
        query = update(self.model).where(self.model.UserID == userId).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def authenticate_user(self, email: str, password: str) -> Result:
        user = await self.get_by_filter_one(Email=email)
        if not user or not verify_password(password, user.PasswordHash):
            return err("Неверные данные для входа или пароль")
        return success(user)

    async def get_by_email(self, email) -> Optional[User]:
        try:
            result = await self._session.execute(select(self.model).where(self.model.Email == email))
            user = result.scalars().first()
            if not user:
                return None
            return user
        except Exception as e:
            return err(str(e))

    async def delete_by_id(self, id) -> Result[int]:
        try:
            result = await self._session.execute(delete(self.model).where(self.model.UserID == id))
            await self._session.commit()
            return success(result.rowcount)
        except Exception as e:
            return err(str(e))
