from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app : FastAPI = FastAPI()

class Blog(BaseModel):
    title : str
    author : str
    read_time : Optional[str]
    


@app.get("/about")
def about():
    return {"data" : {"page": "about-us"}}


@app.get("/getblogs")
def about(limit : str = 10, sort : Optional[str] = None):
    return {"data" : {"page": "getblogs", "limit" : limit, "sort" : sort}}
     
@app.get("/{id}")
def func(id : int):
    return {"user_id" : "OIXM123" ,"name" : "huzaifa", "path_id" : id}

@app.post("/blog")
def create_blog(blog : Blog):

    return {"data" : "blog created", "blog" : {"title" : blog.title, "author" : blog.author, "read_time" : blog.read_time}}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000)
#! The port will not change when you run the application you have to run the main.py file (python main.py)


