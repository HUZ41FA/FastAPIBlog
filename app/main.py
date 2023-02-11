from typing import List
from fastapi import FastAPI
from . import models
from .database import  engine
from sqlalchemy.orm import Session
from .schemas import Blog, ShowBlog, ShowUser, User
from datetime import datetime
from .hash import Hash
from .routers import blogRouter, userRouter, authRouter


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API"
)

app.include_router(blogRouter.router)
app.include_router(userRouter.router)
app.include_router(authRouter.router)
