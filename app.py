from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import registry, Mapped, mapped_column, Session
from sqlalchemy import create_engine

table_registry = registry()
app = FastAPI()
engine = create_engine("sqlite:///database.db")

@table_registry.mapped_as_dataclass()
class User:
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  username: Mapped[str] = mapped_column(init=True)

table_registry.metadata.create_all(engine)

class UserSchema(BaseModel):
  username: str

@app.post("/user")
def create_user(user: UserSchema):
  with Session(engine) as session:
    
    user = User(username=user.username)
    session.add(user)
    session.commit()
    
    return {"msg": "Usuário criado no sistema!"}
