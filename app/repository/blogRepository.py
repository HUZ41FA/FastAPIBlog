from typing import List
from sqlalchemy.orm import Session
from ..models import Blog

def get_all(db : Session) -> List[Blog]:
    return db.query(Blog).all()

def get_by_id(id : int, db : Session) -> Blog:
    return db.query(Blog).filter(Blog.id == id).first()

def create_blog(model : Blog, db:Session) -> bool:
    db.add(model)
    return True

def update_blog(model : Blog, db:Session) -> bool:
    db.query(Blog).update(
            {
                Blog.title : model.title, 
                Blog.body : model.body, 
                Blog.created_by_name : model.created_by_name,
                Blog.created_date : model.created_date
                }
            )

def delete_blog(model: Blog) -> bool:
    model.delete(synchronize_session=False)

    return True