from app.db.db import SessionLocal
from app.db import crud

def display_data():
    
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("ДАННЫЕ ИЗ БАЗЫ ДАННЫХ".center(70))
        print("=" * 70)
        
        categories = crud.get_categories(db)
        print(f"\nКАТЕГОРИИ КНИГ ({len(categories)}):")
        print("-" * 70)
        
        for category in categories:
            print(f"ID: {category.id} | Название: {category.title}")
            
            books = crud.get_books_by_category(db, category.id)
            
            if books:
                print(f"Книги в категории ({len(books)}):")
                for book in books:
                    print(f"  • {book.title}")
                    print(f"    Описание: {book.description[:80]}...")
                    print(f"    Цена: {book.price} руб.")
                    print(f"    Ссылка: {book.url if book.url else 'не указана'}")
                    print()
            else:
                print("  В этой категории пока нет книг")
            
            print("-" * 70)
        
        all_books = crud.get_books(db)
        print(f"\nВСЕ КНИГИ В БАЗЕ ({len(all_books)}):")
        print("-" * 70)
        
        for i, book in enumerate(all_books, 1):
            print(f"{i}. {book.title}")
            print(f"   Категория: {book.category.title}")
            print(f"   Цена: {book.price} руб.")
            print(f"   Описание: {book.description[:100]}...")
            print()
        
        print("\nСТАТИСТИКА:")
        print("-" * 70)
        total_books = len(all_books)
        total_categories = len(categories)
        avg_price = sum(book.price for book in all_books) / total_books if total_books > 0 else 0
        
        print(f"Всего категорий: {total_categories}")
        print(f"Всего книг: {total_books}")
        print(f"Средняя цена книги: {avg_price:.2f} руб.")
        
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        db.close()
        print("\n" + "=" * 70)
        print("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО".center(70))
        print("=" * 70)

if __name__ == "__main__":
    display_data()