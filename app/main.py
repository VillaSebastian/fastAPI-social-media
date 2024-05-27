import time
import logging
from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas import Post
from app.database import set_up_database, get_db

# Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./database.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
logger = logging.getLogger()

set_up_database()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f'Request: {request.method} {request.url.path}, Process Time: {process_time:.4f} seconds')
    return response


@app.get("/")
def root():
    """Serve the index.html file."""
    return FileResponse('./static/index.html')


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """Fetch and return all posts."""
    rows = db.execute(text("SELECT * FROM posts"))
    posts = [{"id": {row.id}, "title": {row.title}, "content": {row.content}, "created_at": {row.created_at}} for row in rows]

    """ conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM posts").fetchall() """
    """ cursor.close()
    conn.close() """
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    """Create a new post."""
    db.execute(text("INSERT INTO posts (title, content) VALUES (:title, :content)"), {"title": post.title, "content": post.content})
    db.commit()
    return {'Message': 'Post created successfully'}


@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    """Fetch and return a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    post = {"id": {row.id}, "title": {row.title}, "content": {row.content}, "created_at": {row.created_at}}
    return {"post_detail": post}


@app.patch("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    """Update a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    db.execute(text("UPDATE posts SET title = :title, content = :content WHERE id = :id"), {"title": updated_post.title, "content": updated_post.content, "id": id})
    db.commit()
    return {"Message": "Post updated successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    """Delete a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    db.execute(text("DELETE FROM posts WHERE id = :id"), {"id": id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)