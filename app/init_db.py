from app.db.db import engine, SessionLocal
from app.db import models
from app.db import crud

def init_database():
    print("Создание таблиц в базе данных")
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Добавление категорий")
        fiction_category = crud.create_category(db, title="Художественная литература")
        programming_category = crud.create_category(db, title="Программирование")
        
        print("Добавление книг в категорию 'Художественная литература'")
        crud.create_book(
            db=db,
            title="Мастер и Маргарита",
            description="Роман Михаила Булгакова",
            price=450.50,
            category_id=fiction_category.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Преступление и наказание",
            description="Роман Фёдора Достоевского",
            price=380.00,
            category_id=fiction_category.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="1984",
            description="Антиутопический роман Джорджа Оруэлла",
            price=520.75,
            category_id=fiction_category.id,
            url=""
        )
        
        print("Добавление книг в категорию 'Программирование'")
        crud.create_book(
            db=db,
            title="Чистый код",
            description="Создание, анализ и рефакторинг",
            price=1200.00,
            category_id=programming_category.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Совершенный код",
            description="Полное руководство по созданию качественного ПО",
            price=1500.50,
            category_id=programming_category.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Грокаем алгоритмы",
            description="Иллюстрированное пособие для программистов",
            price=890.00,
            category_id=programming_category.id,
            url=""
        )
        
        crud.create_book(
            db=db,
            title="Python. К вершинам мастерства",
            description="Продвинутое программирование на Python",
            price=1100.25,
            category_id=programming_category.id,
            url=""
        )
        
        print("База данных успешно инициализирована!")
        print(f"Добавлено категорий: 2")
        print(f"Добавлено книг: 7")
        
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()