from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    Name: str
    Description: str
    Price: float
    CategoryID: int
    Status: bool

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    ItemID: int

    class Config:
        orm_mode = True
