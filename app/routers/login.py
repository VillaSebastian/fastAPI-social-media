import app.schemas as schemas
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import verify_password
from app.security import create_access_token
from app.schemas import Token

router = APIRouter(
    prefix="/login",
    tags=['Login']
)

@router.post("", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": user_credentials.username}).fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    elif not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer", "url": "/view/posts"},
                        status_code=status.HTTP_200_OK)