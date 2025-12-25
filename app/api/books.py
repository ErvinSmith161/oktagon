from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, models
from app.db.db import get_db_session
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.api.categories import read_category

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    db: Session = Depends(get_db_session)
):
    """Получить список книг с возможностью фильтрации по категории"""
    if category_id:
        category = crud.get_category_by_id(db, category_id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found"
            )
        books = crud.get_books_by_category(db, category_id=category_id)
    else:
        books = crud.get_books(db, skip=skip, limit=limit)
    
    for book in books:
        book.category = book.category
    return books

@router.get("/{book_id}", response_model=BookResponse)
def read_book(
    book_id: int, 
    db: Session = Depends(get_db_session)
):
    """Получить книгу по ID"""
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    db_book.category = db_book.category
    return db_book

@router.post(
    "/", 
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: BookCreate, 
    db: Session = Depends(get_db_session)
):
    """Создать новую книгу"""
    category = crud.get_category_by_id(db, category_id=book.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {book.category_id} not found"
        )
    
    db_book = crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )
    
    db_book.category = category
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, 
    book: BookUpdate, 
    db: Session = Depends(get_db_session)
):
    """Обновить книгу"""
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    if book.category_id is not None:
        category = crud.get_category_by_id(db, category_id=book.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {book.category_id} not found"
            )
    
    update_data = book.dict(exclude_unset=True)
    updated_book = crud.update_book(db=db, book_id=book_id, **update_data)
    
    updated_book = crud.get_book_by_id(db, book_id=book_id)
    updated_book.category = updated_book.category
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db_session)
):
    """Удалить книгу"""
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    crud.delete_book(db=db, book_id=book_id)
    return None