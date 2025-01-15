from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str
    author: str
    description: str

class UpdateBookSchema(BaseModel):
    title: str | None = Field(None)
    author: str | None = Field(None)
    description: str | None = Field(None)
 