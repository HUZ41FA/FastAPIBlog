from typing import List
from fastapi import APIRouter, FastAPI, Depends, status, Response, HTTPException
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Blog, ShowBlog, ShowUser, User
from datetime import datetime
from ..hash import Hash
from ..repository import blogRepository

router = APIRouter(
    tags=['Blog'],
    prefix='/blog'
)



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
async def create(request : Blog, db : Session = Depends(get_db)):

    new_blog = models.Blog(
        title=request.title, 
        body=request.body, 
        user_id = request.user_id,
        created_by_name = "huzaifa", 
        created_date = datetime.now()
        )
    
    blogRepository.create_blog(new_blog, db)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowBlog)
async def get_blog_by_id(id : int, response : Response , db : Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()   
    
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found")
    return blog

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowBlog])
async def get_all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_by_id(id : int, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with Id:{id} does not exists")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"message" : "Blog updated successfully"}
    
@router.put("/{id}", status_code=status.HTTP_200_OK)
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
