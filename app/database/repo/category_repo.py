from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Category
from app.database.abstract.abc_repo import AbstractRepository
from sqlalchemy import select, insert, delete, update
from app.utils.result import Result, err, success

class CategoryRepository(AbstractRepository):
    model = Category

    async def create(self, **kwargs):
        query = insert(self.model).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self.commit()
        return result.scalars().first()

    async def update_by_id(self, category_id: int, **kwargs):
        query = update(self.model).where(self.model.CategoryID == category_id).values(**kwargs).returning(self.model)
        result = await self._session.execute(query)
        await self.commit()
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Category]:
        try:
            result = await self._session.execute(select(self.model).where(self.model.CategoryName == name))
            category = result.scalars().first()
            if not category:
                return None
            return category
        except Exception as e:
            return err(str(e))

    async def delete_by_id(self, category_id: int) -> Result[int]:
        try:
            result = await self._session.execute(delete(self.model).where(self.model.CategoryID == category_id))
            await self.commit()
            return success(result.rowcount)
        except Exception as e:
            return err(str(e))
