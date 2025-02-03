from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Category
from app.database.repo.category_repo import CategoryRepository
from app.utils.result import Result, err, success
from app.schems.request.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: CategoryRepository = CategoryRepository(session)

    async def create_category(self, category_request: CategoryCreate) -> Result[Category]:
        try:
            inserted = await self._repo.create(CategoryName=category_request.CategoryName)
            await self._repo.commit()
            return success(inserted)
        except Exception as e:
            return err(str(e))

    async def get_categories(self, skip: int = 0, limit: int = 10) -> Result[List[Category]]:
        categories = await self._repo.get_all()
        return success(categories)

    async def get_category_by_id(self, category_id: int) -> Result[Category]:
        category = await self._repo.get_by_id(category_id)
        return success(category) if category else err("Category not found")

    async def update_category(self, category_id: int, category_request: CategoryUpdate) -> Result[Category]:
        try:
            updated = await self._repo.update_by_id(category_id, CategoryName=category_request.CategoryName)
            await self._repo.commit()
            return success(updated)
        except Exception as e:
            return err(str(e))

    async def delete_category(self, category_id: int) -> Result[int]:
        result = await self._repo.delete_by_id(category_id)
        return result
