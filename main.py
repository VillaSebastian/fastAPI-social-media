from fastapi import FastAPI, Response, status, HTTPException
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    post['id'] = randint(1, 1000000)
    posts_examples.append(post)
    return {'post created:': f'title {post["title"]} content: {post["content"]}'}

@app.get("/posts/{id}")
def get_one_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'post with id {id} was not found')  
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    posts_examples.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/posts/{id}")
def update_post(id: int, updated_post: Post):
    for post in posts_examples:
        if post['id'] == id:
            post['title'] = updated_post.title
            post['content'] = updated_post.content
    return {"Message": "Post updated succesfully"}