from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import registry, Mapped, mapped_column, Session
from sqlalchemy import create_engine, select, update, delete

# Configurações Gerais da aplicação
table_registry = registry()
app = FastAPI()
engine = create_engine("sqlite:///database.db")

# Definição das tabelas do banco de dados
@table_registry.mapped_as_dataclass()
class User:
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  username: Mapped[str] = mapped_column(init=True)

table_registry.metadata.create_all(engine)


# Definição dos schemas da aplicação
class UserSchema(BaseModel):
  username: str

class UpdateUserSchema(BaseModel):
  new_username: str


# Definição dos endpoints da aplicação
@app.get("/")
def ping():
  return "O programa está funcionando!"

@app.post("/user")
def create_user(user: UserSchema):
  with Session(engine) as session:
    
    user = User(username=user.username)
    session.add(user)
    session.commit()
    
    return {"msg": "Usuário criado no sistema!"}

@app.get("/user/{id}")
def get_user(id: int):
  stmt = select(User).where(User.id == id)

  with Session(engine) as session:
    user = session.execute(statement=stmt).scalar_one_or_none()

    if not user:
      raise HTTPException(status_code=422, detail="Usuário não encontrado no sistema!")

    return user

@app.get("/users")
def get_users():
  stmt = select(User)

  with Session(engine) as session:
    users = session.execute(statement=stmt).scalars().fetchall()

    return users

@app.put("/user/{id}")
def update_user(id: int, user_payload: UpdateUserSchema):
  stmt = update(User).where(User.id == id).values(username=user_payload.new_username)

  with Session(engine) as session:
    session.execute(stmt)
    session.commit()

    return {"msg": "Usuário atualizado com sucesso!"}

@app.delete("/user/{id}")
def delete_user(id: int):
  stmt = delete(User).where(User.id == id)

  with Session(engine) as session:
    session.execute(stmt)
    session.commit()

    return {"msg": "Usuário deletado com sucesso!"}