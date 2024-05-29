import app.schemas as schemas
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new User by email and password"""
    db.execute(text("INSERT INTO users (email, password) VALUES (:email, :password)"),
                    {"email": user.email, "password": user.password})
    db.commit()
    new_user = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": user.email}).fetchone()
    if new_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_one_user(id: int, db: Session = Depends(get_db)):
    """Get one user's info by its id"""
    existing_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=400, detail=f'User with id: {id} was not found')
    return existing_user


@router.patch("/{id}", response_model=schemas.User)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete an existing user"""
    existing_user = db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id}).fetchone()
    if existing_user is None:
        raise HTTPException(status_code=400, detail=f'User with id: {id} was not found')
    db.execute(text("DELETE FROM users WHERE id = :id"), {"id": id})
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)