from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

posts_examples = [{'title': 'This is my first post', 'content': 'some interesting content'}, {'title': 'A clickbait title', 'content': 'Generic content'}]

@app.get("/")
def root():
    return FileResponse('./static/index.html')

@app.get("/posts")
def get_posts():
    return {'data': posts_examples}