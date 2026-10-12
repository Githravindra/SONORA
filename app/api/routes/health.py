from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    return {"status": "ok", "service": "SONORA backend"}


@router.get("/db")
def db_health(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
