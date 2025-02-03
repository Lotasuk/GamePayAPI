from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.connector import get_session
from app.database.models.models import Order, OrderItem
from pydantic import BaseModel
from app.services.order_service import OrderService
from app.schems.request.order import OrderCreateRequest, OrderResponse

order_router = APIRouter(prefix="/orders", tags=["Orders"])

@order_router.post("/", response_model=dict)
async def create_order(
    order_data: OrderCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    result = await service.create_order(order_data)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    return {"order_id": result["value"]}

@order_router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    result = await service.get_orders_by_user(user_id)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    return result["value"]

@order_router.get("/{order_id}", response_model=dict)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    result = await service.get_order_details(order_id)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    return result["value"]