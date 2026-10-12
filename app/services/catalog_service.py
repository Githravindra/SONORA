from typing import Any

from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email: str, username: str, password: str) -> dict[str, Any]:
        if self.db.query(User).filter(User.email == email).first():
            raise ValueError("User already exists")
        if self.db.query(User).filter(User.username == username).first():
            raise ValueError("Username already taken")
        user = User(email=email, username=username, password_hash=get_password_hash(password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {
            "user_id": user.id,
            "access_token": create_access_token(user.email),
            "token_type": "bearer",
        }

    def login(self, email: str, password: str) -> dict[str, Any]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return {
            "user_id": user.id,
            "access_token": create_access_token(user.email),
            "token_type": "bearer",
        }
