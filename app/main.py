from fastapi import FastAPI
from . import models
from .database import  engine
from .routers import blogRouter, userRouter, authRouter


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    
)

app.include_router(blogRouter.router)
app.include_router(userRouter.router)
app.include_router(authRouter.router)
