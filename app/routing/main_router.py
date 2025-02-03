from fastapi import APIRouter, HTTPException
from app.routing.auth_router import auth_router
from app.routing.item_router import item_router
from app.routing.category_router import category_router
from app.routing.order_router import order_router

main_router = APIRouter(
    prefix="/test",
)



main_router.include_router(auth_router)
main_router.include_router(item_router)
main_router.include_router(category_router)
main_router.include_router(order_router)