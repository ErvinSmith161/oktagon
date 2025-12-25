from fastapi import FastAPI
from app.api import books, categories

app = FastAPI(title="Book API")

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Book API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}