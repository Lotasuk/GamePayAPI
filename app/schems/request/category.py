from pydantic import BaseModel

class CategoryBase(BaseModel):
    CategoryName: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    CategoryID: int

    class Config:
        orm_mode = True
