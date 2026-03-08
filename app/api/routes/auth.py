from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.auth_schema import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "name": current_user.name,
        "role": current_user.role,
        "email": current_user.email,
        "phone": current_user.phone,
        "verified": current_user.verified,
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.phone == user.phone)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": str(new_user.id)})

    return {"access_token": access_token}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.phone == user.phone)
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": access_token}
