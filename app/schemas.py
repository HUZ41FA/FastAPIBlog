from typing import List
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class User(BaseModel):
    username : str
    email : str
    password : str

class BlogBase(BaseModel):
    title: str
    body : str
    user_id : int
    
class Blog(BlogBase):
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    username : str
    email : str
    blogs : List[Blog]

    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title : str
    body : str
    creator : ShowUser

    class Config:
        orm_mode = True



class Login(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class LoginUser(BaseModel):
    email : str
    username : str
    access_token : str
    token_type : str