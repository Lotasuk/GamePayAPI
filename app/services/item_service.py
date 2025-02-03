from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Item
from app.database.repo.item_repo import ItemRepository
from app.utils.result import Result, err, success
from app.schems.request.item import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repo: ItemRepository = ItemRepository(session)

    async def create_item(self, item_request: ItemCreate) -> Result[Item]:
        try:
            inserted = await self._repo.create(
                Name=item_request.Name,
                Description=item_request.Description,
                Price=item_request.Price,
                CategoryID=item_request.CategoryID,
                Status=item_request.Status
            )
            await self._repo.commit()
            return success(inserted)
        except Exception as e:
            return err(str(e))

    async def get_items(self, skip: int = 0, limit: int = 10) -> Result[List[Item]]:
        items = await self._repo.get_all()
        return success(items)

    async def get_item_by_id(self, item_id: int) -> Result[Item]:
        item = await self._repo.get_by_id(item_id)
        return success(item) if item else err("Item not found")

    async def update_item(self, item_id: int, item_request: ItemUpdate) -> Result[Item]:
        try:
            updated = await self._repo.update_by_id(
                item_id,
                Name=item_request.Name,
                Description=item_request.Description,
                Price=item_request.Price,
                CategoryID=item_request.CategoryID,
                Status=item_request.Status
            )
            await self._repo.commit()
            return success(updated)
        except Exception as e:
            return err(str(e))

    async def delete_item(self, item_id: int) -> Result[int]:
        result = await self._repo.delete_by_id(item_id)
        return result
