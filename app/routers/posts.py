import app.schemas as schemas
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    """Fetch and return all posts."""
    rows = db.execute(text("SELECT * FROM posts"))
    posts = [{"id": {row.id},
              "title": {row.title},
              "content": {row.content},
              "created_at": {row.created_at}}
              for row in rows]
    return {'data': posts}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create a new post."""
    db.execute(text("INSERT INTO posts (title, content) VALUES (:title, :content)"),
               {"title": post.title, "content": post.content})
    db.commit()
    return {'Message': 'Post created successfully'}


@router.get("/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    """Fetch and return a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    post = {"id": {row.id}, "title": {row.title}, "content": {row.content}, "created_at": {row.created_at}}
    return {"post_detail": post}


@router.patch("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    db.execute(text("UPDATE posts SET title = :title, content = :content WHERE id = :id"),
               {"title": updated_post.title, "content": updated_post.content, "id": id})
    db.commit()
    return {"Message": "Post updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    """Delete a post by ID."""
    row = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    db.execute(text("DELETE FROM posts WHERE id = :id"), {"id": id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)