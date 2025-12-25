from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import crud, models
from app.db.db import get_db_session
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db_session)
):
    """Получить список всех категорий"""
    categories = crud.get_categories(db, skip=skip, limit=limit)
    for category in categories:
        category.books_count = len(category.books)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: int, 
    db: Session = Depends(get_db_session)
):
    """Получить категорию по ID"""
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    db_category.books_count = len(db_category.books)
    return db_category

@router.post(
    "/", 
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db_session)
):
    """Создать новую категорию"""
    existing_category = db.query(models.Category).filter(
        models.Category.title == category.title
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this title already exists"
        )
    
    return crud.create_category(db=db, title=category.title)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: Session = Depends(get_db_session)
):
    """Обновить категорию"""
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    if category.title is not None:
        existing = db.query(models.Category).filter(
            models.Category.title == category.title,
            models.Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this title already exists"
            )
    
    updated_category = crud.update_category(
        db=db, 
        category_id=category_id, 
        title=category.title
    )
    updated_category.books_count = len(updated_category.books)
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db_session)
):
    """Удалить категорию"""
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    
    if len(db_category.books) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with books. Delete books first."
        )
    
    crud.delete_category(db=db, category_id=category_id)
    return None