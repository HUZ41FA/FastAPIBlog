from sqlalchemy.orm import Session
from models.blog import Blog
from datetime import datetime

class BlogService:
    db_session : Session

    def __init__(self, db_session : Session):
        self.db_session = db_session

    def create_blog(self, model : Blog) -> bool:
        model.created_by_name = "Huzaifa Khan"
        model.created_date = datetime.now()

        self.db_session.add(instance=model)

        return True    
