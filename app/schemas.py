from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True  # optional with default value

class PostCreate(PostBase):
  pass

class PostResponse(PostBase):
  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserReponse(BaseModel):
  email: EmailStr
  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None

