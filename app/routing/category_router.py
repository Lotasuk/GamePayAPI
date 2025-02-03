from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Category
from app.database.repo.category_repo import CategoryRepository
from app.schems.request.category import CategoryCreate, CategoryUpdate, Category
from app.database.abstract.abc_repo import AbstractRepository
from app.database.connector import get_session
from app.services.category_service import CategoryService
from typing import List

category_router = APIRouter(prefix="/category", tags=["Category"])

@category_router.post("/", response_model=Category)
async def create_category(request: CategoryCreate, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    result = await service.create_category(request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@category_router.get("/", response_model=List[Category])
async def read_categories(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    result = await service.get_categories(skip=skip, limit=limit)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@category_router.get("/{category_id}", response_model=Category)
async def read_category(category_id: int, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    result = await service.get_category_by_id(category_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return result.value

@category_router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, request: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    result = await service.update_category(category_id, request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value

@category_router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    result = await service.delete_category(category_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return {"detail": "Category deleted"}