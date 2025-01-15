from pydantic import BaseModel

class UserSchema(BaseModel):
  username: str

class UpdateUserSchema(BaseModel):
  new_username: str