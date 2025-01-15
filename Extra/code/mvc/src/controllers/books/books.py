from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import Session
from config.database import engine
from .booksSchema import UpdateBookSchema, BookSchema
from models.book import Book

book_router = APIRouter(tags=["Books"])


@book_router.post("/book", status_code=201)
def create_book(book_payload: BookSchema):
  with Session(engine) as session:
    
    query = insert(Book).values(
       title=book_payload.title, 
       author=book_payload.author,
       description=book_payload.description 
    )

    session.execute(statement=query)
    session.commit()

    return book_payload
  
@book_router.get("/books", status_code=200)
def read_books():
   with Session(engine) as session:
      query = select(Book)

      books = session.execute(statement=query).scalars().all()
      
      return books

@book_router.get("/book/{book_id}")
def find_book_by_id(book_id: int):
    with Session(engine) as session:
        query = select(Book).where(Book.id == book_id)

        has_book = session.execute(statement=query).scalar_one_or_none()

        if not has_book:
            raise HTTPException(status_code=404, detail="O livro buscado não está cadastrado!")

        book = has_book
        
        return book

@book_router.put("/book/{book_id}")
def update_book(book_id: int, book_payload: UpdateBookSchema):
    with Session(engine) as session:
        query = select(Book).where(Book.id == book_id)

        has_book = session.execute(statement=query).scalar_one_or_none()

        if not has_book:
            raise HTTPException(status_code=404, detail="O livro buscado não está cadastrado!")
        
        values_to_update = {}

        if book_payload.title is not None:
            values_to_update["title"] = book_payload.title

        if book_payload.author is not None:
            values_to_update["author"] = book_payload.author

        if book_payload.description is not None:
            values_to_update["description"] = book_payload.description

        if not values_to_update:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar foi fornecido.")

        query = update(Book).where(Book.id == book_id).values(**values_to_update)
        session.execute(query)
        session.commit()

        return {"message": "Livro atualizado com sucesso!"}