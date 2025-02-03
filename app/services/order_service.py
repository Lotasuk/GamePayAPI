from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.connector import get_session
from app.database.models.models import Order, OrderItem
from pydantic import BaseModel
from sqlalchemy import select
from app.schems.request.order import OrderCreateRequest
class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order_data: OrderCreateRequest):
        try:
            # Создаем заказ
            new_order = Order(
                UserID=order_data.UserID,
                CreationDate=order_data.CreationDate,
                Status=order_data.Status
            )
            self.session.add(new_order)
            await self.session.flush()

            # Добавляем элементы заказа
            for item in order_data.Items:
                new_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemID=item.ItemID,
                    Quantity=item.Quantity
                )
                self.session.add(new_item)

            await self.session.commit()
            return {"success": True, "value": new_order.OrderID}
        
        except Exception as e:
            await self.session.rollback()
            return {"success": False, "error": str(e)}

    async def get_orders_by_user(self, user_id: int):
        try:
            result = await self.session.execute(
                select(Order).where(Order.UserID == user_id)
            )
            orders = result.scalars().all()
            return {"success": True, "value": orders}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_order_details(self, order_id: int):
        try:
            # Получаем заказ
            order_result = await self.session.execute(
                select(Order).where(Order.OrderID == order_id)
            )
            order = order_result.scalar_one_or_none()

            if not order:
                return {"success": False, "error": "Order not found"}

            # Получаем элементы заказа
            items_result = await self.session.execute(
                select(OrderItem).where(OrderItem.OrderID == order_id)
            )
            items = items_result.scalars().all()

            return {
                "success": True,
                "value": {
                    "order": order,
                    "items": items
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}