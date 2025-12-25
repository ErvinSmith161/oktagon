from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название категории")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название категории")

class CategoryResponse(CategoryBase):
    id: int
    books_count: Optional[int] = None
    
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: float = Field(..., gt=0, description="Цена книги (больше 0)")
    url: Optional[str] = Field(None, max_length=500, description="Ссылка на товар")
    category_id: int = Field(..., description="ID категории")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    category: Optional[CategoryResponse] = None
    
    class Config:
        from_attributes = True