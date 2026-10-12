from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import ListeningHistory, Track, User
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    service = AnalyticsService(db)
    return service.overview_for_user(current_user.id)


@router.get("/top-tracks")
def top_tracks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
) -> list[dict[str, Any]]:
    service = AnalyticsService(db)
    return service.top_tracks(current_user.id, limit)
