from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create(blog : schemas.Blog, db : Session = Depends(get_db)):
    new_blog : models.Blog = models.Blog(title=blog.title, body=blog.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get("/blog", status_code=status.HTTP_200_OK)
async def get_all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def get_blog_by_id(id, response : Response , db : Session = Depends(get_all)):
    print(id)
    blog = db.query(models.Blog).all()    
    
    if blog:
        return blog

    response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found")
