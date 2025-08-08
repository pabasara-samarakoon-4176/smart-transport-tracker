from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(user_data: schemas.RegisterSchema, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user_data.password)

    new_user = models.User(
        name=user_data.name,
        phone=user_data.phone,
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully.", "user_id": new_user.id}

@router.post("/login")
def login_user(user_data: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return {"message": "Login successful", "user_id": user.id}