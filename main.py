from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from random import randint

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

class Post(BaseModel):
    title: str
    content: str

posts_examples = [{'title': 'This is my first post', 'content': 'some interesting content','id': 1}, {'title': 'A clickbait title', 'content': 'Generic content','id': 2}]

def find_post(id):
    for post in posts_examples:
        if post['id'] == id:
            return post

@app.get("/")
def root():
    return FileResponse('./static/index.html')

@app.get("/posts")
def get_posts():
    return {'data': posts_examples}

@app.post("/posts")
def create_post(post: Post):
    post = post.dict()
    post['id'] = randint(1, 1000000)
    posts_examples.append(post)
    return {'post created:': f'title {post["title"]} content: {post["content"]}'}

@app.get("/posts/{id}")
def get_one_post(id: int):
    post = find_post(id)
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id)
    if post:
        posts_examples.remove(post)
    return {"Post removed succesfully"}