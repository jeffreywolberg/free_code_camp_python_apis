from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# schema for data to expect user to send when logging in/creating account
class UserCreate(BaseModel):
  email: EmailStr
  password: str

# schema for how to return User data back to user
class UserResponse(BaseModel):
  email: EmailStr
  class Config:
    orm_mode = True

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True  # optional with default value

# schema for how to expect post data to come in from user
class PostCreate(PostBase):
  pass

# schema for how to return post data to user
class PostResponse(PostBase):
  class Config:
    orm_mode = True
  id: int
  created_at: datetime  
  owner_id: int
  owner: UserResponse

# schema for data to expect when token is sent from user
class Token(BaseModel):
  access_token: str
  token_type: str

# schema for how to return token data after verifying it
class TokenData(BaseModel):
  id: Optional[str] = None

