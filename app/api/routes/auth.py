from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models import User, UserProfile, SearchHistory
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.flush()

    profile = UserProfile(user_id=user.id, display_name=payload.username)
    db.add(profile)
    db.commit()
    db.refresh(user)

    access = create_access_token(user.email)
    return {"access_token": access, "token_type": "bearer"}


@router.post("/login", response_model=TokenPair)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access = create_access_token(user.email)
    return {"access_token": access, "token_type": "bearer"}


@router.get("/me")
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "profile": {
            "display_name": profile.display_name if profile else current_user.username,
            "theme": profile.theme if profile else "dark",
            "accent": profile.accent if profile else "purple",
            "autoplay": profile.autoplay if profile else True,
        },
    }


@router.get("/search-history")
def recent_searches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[str]:
    rows = db.query(SearchHistory.query).filter(SearchHistory.user_id == current_user.id).order_by(SearchHistory.created_at.desc()).limit(10).all()
    return [row[0] for row in rows]
