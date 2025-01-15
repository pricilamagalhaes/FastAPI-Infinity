from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import Session
from config.database import engine
from .userSchema import UserSchema, UpdateUserSchema
from models.user import User

user_router = APIRouter(tags=["Users"])

@user_router.post("/user")
def create_user(user: UserSchema):
  with Session(engine) as session:
    
    user = User(username=user.username)
    session.add(user)
    session.commit()
    
    return {"msg": "Usuário criado no sistema!"}

@user_router.get("/user/{id}")
def get_user(id: int):
  stmt = select(User).where(User.id == id)

  with Session(engine) as session:
    user = session.execute(statement=stmt).scalar_one_or_none()

    if not user:
      raise HTTPException(status_code=422, detail="Usuário não encontrado no sistema!")

    return user

@user_router.get("/users")
def get_users():
  stmt = select(User)

  with Session(engine) as session:
    users = session.execute(statement=stmt).scalars().fetchall()

    return users

@user_router.put("/user/{id}")
def update_user(id: int, user_payload: UpdateUserSchema):
  stmt = update(User).where(User.id == id).values(username=user_payload.new_username)

  with Session(engine) as session:
    session.execute(stmt)
    session.commit()

    return {"msg": "Usuário atualizado com sucesso!"}

@user_router.delete("/user/{id}")
def delete_user(id: int):
  stmt = delete(User).where(User.id == id)

  with Session(engine) as session:
    session.execute(stmt)
    session.commit()

    return {"msg": "Usuário deletado com sucesso!"}