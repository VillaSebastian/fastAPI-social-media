import app.schemas as schemas
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """Fetch and return all posts."""
    posts = db.execute(text("SELECT * FROM posts")).fetchall()
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Create a new post."""
    post = db.execute(text("INSERT INTO posts (title, content, user_id) VALUES (:title, :content, :user_id) RETURNING *"),
                        {"title": post.title, "content": post.content, "user_id": current_user.id}).fetchone()
    db.commit()
    return post


@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    """Fetch and return a post by ID."""
    post = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    return post


@router.patch("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update a post by ID."""
    existing_post = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    updated_post = db.execute(text("UPDATE posts SET title = :title, content = :content WHERE id = :id RETURNING *"),
                            {"title": updated_post.title, "content": updated_post.content, "id": id}).fetchone()
    db.commit()
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Delete a post by ID."""
    post = db.execute(text("SELECT * FROM posts WHERE id = :id"), {"id": id}).fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post {id} was not found')
    elif post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested action")
    db.execute(text("DELETE FROM posts WHERE id = :id"), {"id": id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)