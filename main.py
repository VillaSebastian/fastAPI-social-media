from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

class Post(BaseModel):
    title: str
    content: str

posts_examples = [{'title': 'This is my first post', 'content': 'some interesting content'}, {'title': 'A clickbait title', 'content': 'Generic content'}]

@app.get("/")
def root():
    return FileResponse('./static/index.html')

@app.get("/posts")
def get_posts():
    return {'data': posts_examples}

@app.post("/posts")
def create_post(post: Post):
    return {'post created:': f'title {post.title} content: {post.content}'}