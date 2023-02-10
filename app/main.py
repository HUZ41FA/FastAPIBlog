from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .schemas import Blog, ShowBlog, ShowUser, User
from datetime import datetime
from .hash import Hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=ShowBlog, tags=['Blog'])
async def create(request : Blog, db : Session = Depends(get_db)):

    new_blog = models.Blog(
        title=request.title, 
        body=request.body, 
        user_id = request.user_id,
        created_by_name = "huzaifa", 
        created_date = datetime.now()
        )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=['Blog'])
async def get_blog_by_id(id : int, response : Response , db : Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()   
    
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found")
    return blog

@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[ShowBlog], tags=['Blog'])
async def get_all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs
    
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
async def delete_blog_by_id(id : int, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with Id:{id} does not exists")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"message" : "Blog updated successfully"}
    
@app.put("/blog/{id}", status_code=status.HTTP_200_OK, tags=['Blog'])
async def update_blog_by_id(id : int, requestBlog: Blog, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
            return False
    db.query(models.Blog).update(
            {
                models.Blog.title : requestBlog.title, 
                models.Blog.body : requestBlog.body, 
                models.Blog.created_by_name : blog.created_by_name,
                models.Blog.created_date : blog.created_date
                }
            )
    db.commit()

    return {"message" : "Blog updated successfully"}


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['User'])
async def create_user(user : User, db : Session = Depends(get_db)):
    user.password = Hash.hash_bcrypt(user.password)
    new_user = models.User(username = user.username, email = user.email, password = user.password, created_date = datetime.now())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['User'])
async def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")
    return user
