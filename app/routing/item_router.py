from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Item
from app.database.repo.item_repo import ItemRepository
from app.schems.request.item import ItemCreate, ItemUpdate, Item
from app.database.abstract.abc_repo import AbstractRepository
from app.database.connector import get_session
from app.services.item_service import ItemService
from typing import List

item_router = APIRouter(prefix="/item", tags=["Item"])

@item_router.post("/", response_model=Item)
async def create_item(request: ItemCreate, session: AsyncSession = Depends(get_session)):
    service = ItemService(session)
    result = await service.create_item(request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@item_router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    service = ItemService(session)
    result = await service.get_items(skip=skip, limit=limit)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@item_router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    service = ItemService(session)
    result = await service.get_item_by_id(item_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return result.value

@item_router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, request: ItemUpdate, session: AsyncSession = Depends(get_session)):
    service = ItemService(session)
    result = await service.update_item(item_id, request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@item_router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    service = ItemService(session)
    result = await service.delete_item(item_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return {"detail": "Item deleted"}