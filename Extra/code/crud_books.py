from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import registry, Session
from sqlalchemy import select, update, delete, insert

app = FastAPI()
engine = create_engine("sqlite:///books.db")
table_registry = registry()

@table_registry.mapped_as_dataclass()
class Book:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(init=True)
    author: Mapped[str] = mapped_column(init=True)
    description: Mapped[str] = mapped_column(init=True)


table_registry.metadata.create_all(engine)

class BookSchema(BaseModel):
    title: str
    author: str
    description: str

class UpdateBookSchema(BaseModel):
    title: str | None = Field(None)
    author: str | None = Field(None)
    description: str | None = Field(None)
 

@app.post("/book", status_code=201)
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
  
@app.get("/books", status_code=200)
def read_books():
   with Session(engine) as session:
      query = select(Book)

      books = session.execute(statement=query).scalars().all()
      
      return books

@app.get("/book/{book_id}")
def find_book_by_id(book_id: int):
    with Session(engine) as session:
        query = select(Book).where(Book.id == book_id)

        has_book = session.execute(statement=query).scalar_one_or_none()

        if not has_book:
            raise HTTPException(status_code=404, detail="O livro buscado não está cadastrado!")

        book = has_book
        
        return book

@app.put("/book/{book_id}")
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