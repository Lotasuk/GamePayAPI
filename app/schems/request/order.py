from pydantic import BaseModel
from typing import List, Optional
from datetime import date
class OrderItemCreate(BaseModel):
    ItemID: int
    Quantity: int

class OrderCreateRequest(BaseModel):
    UserID: int
    CreationDate: date
    Status: str
    Items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    OrderID: int
    UserID: int
    CreationDate: date
    Status: str
    Items: List[OrderItemCreate]