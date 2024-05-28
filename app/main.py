import time
import logging
import app.schemas as schemas
from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
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
    posts = [{"id": {row.id},
              "title": {row.title},
              "content": {row.content},
              "created_at": {row.created_at}}
              for row in rows]
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create a new post."""
    db.execute(text("INSERT INTO posts (title, content) VALUES (:title, :content)"),
               {"title": post.title, "content": post.content})
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
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    db.execute(text("UPDATE posts SET title = :title, content = :content WHERE id = :id"),
               {"title": updated_post.title, "content": updated_post.content, "id": id})
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


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new User by email and password"""
    db.execute(text("INSERT INTO users (email, password) VALUES (:email, :password)"),
                    {"email": user.email, "password": user.password})
    db.commit()
    new_user = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": user.email}).fetchone()
    if new_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return new_user


@app.get("/users/{id}", response_model=schemas.User)
def get_one_user(id: int, db: Session = Depends(get_db)):
    """Get one user's info by its id"""
    existing_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=400, detail=f'User with id: {id} was not found')
    return existing_user


@app.patch("/users/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Update an existing user's information"""
    existing_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=400, detail=f'User with id: {id} was not found')
    db.execute(text("UPDATE users SET email = :email, password = :password WHERE id = :id"),
                    {"email": user.email, "password": user.password, "id": id})
    db.commit()
    updated_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    return updated_user


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete an existing user"""
    existing_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=400, detail=f'User with id: {id} was not found')
    db.execute(text("DELETE FROM users WHERE id = :id"), {"id": id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)