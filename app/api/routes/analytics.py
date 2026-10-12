from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Track, User
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/discovery", tags=["discovery"])


@router.get("/recommendations")
def personalized_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
) -> list[dict[str, Any]]:
    service = RecommendationService(db)
    return service.personalized_recommendations(current_user.id, limit)


@router.get("/trending")
def trending_tracks(db: Session = Depends(get_db), limit: int = Query(10, ge=1, le=30)) -> list[dict[str, Any]]:
    rows = db.query(Track).order_by(Track.play_count.desc()).limit(limit).all()
    return [{"id": row.id, "title": row.title, "play_count": row.play_count} for row in rows]


@router.get("/similar/{track_id}")
def similar_tracks(track_id: str, db: Session = Depends(get_db), limit: int = Query(5, ge=1, le=20)) -> list[dict[str, Any]]:
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        return []
    rows = db.query(Track).filter(Track.id != track_id, Track.genre_id == track.genre_id).limit(limit).all()
    return [{"id": row.id, "title": row.title, "genre": row.genre.name if row.genre else None} for row in rows]
