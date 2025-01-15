from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import registry, Session

from models.book import Book
from config.database import engine, table_registry
from controllers.books.books import book_router
from controllers.users.user import user_router

def create_app() -> FastAPI:
    app = FastAPI(debug=True)

    app.include_router(book_router)
    app.include_router(user_router)

    table_registry.metadata.create_all(engine)

    return app


app = create_app()