from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import ListeningHistory, PlaybackEvent, Track, User

router = APIRouter(prefix="/playback", tags=["playback"])


@router.post("/start")
def record_playback_start(payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    track_id = payload.get("track_id")
    if not track_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="track_id is required")
    db.add(PlaybackEvent(user_id=current_user.id, track_id=track_id, event_type="start"))
    db.commit()
    return {"status": "recorded", "event_type": "start", "track_id": track_id}


@router.post("/progress")
def record_playback_progress(payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    track_id = payload.get("track_id")
    if not track_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="track_id is required")
    db.add(PlaybackEvent(user_id=current_user.id, track_id=track_id, event_type="progress", position_seconds=payload.get("position_seconds", 0)))
    db.commit()
    return {"status": "recorded", "event_type": "progress", "track_id": track_id}


@router.post("/complete")
def record_playback_complete(payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    track_id = payload.get("track_id")
    if not track_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="track_id is required")
    track = db.query(Track).filter(Track.id == track_id).first()
    if track:
        track.play_count += 1
    db.add(PlaybackEvent(user_id=current_user.id, track_id=track_id, event_type="complete", duration_seconds=payload.get("duration_seconds", 0)))
    db.add(ListeningHistory(user_id=current_user.id, track_id=track_id, duration_seconds=payload.get("duration_seconds", 0), completion_ratio=100))
    db.commit()
    return {"status": "recorded", "event_type": "complete", "track_id": track_id}


@router.get("/history")
def playback_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = Query(20, ge=1, le=100)) -> list[dict[str, Any]]:
    rows = db.query(ListeningHistory).filter(ListeningHistory.user_id == current_user.id).order_by(ListeningHistory.played_at.desc()).limit(limit).all()
    return [{"id": row.id, "track_id": row.track_id, "title": row.track.title if row.track else None, "played_at": row.played_at.isoformat(), "duration_seconds": row.duration_seconds} for row in rows]


@router.get("/queue")
def get_queue(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {"queue": [], "user_id": current_user.id}


@router.post("/queue")
def save_queue(payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {"status": "saved", "queue": payload.get("tracks", [])}


@router.get("/availability/{track_id}")
def track_availability(track_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return {"track_id": track.id, "status": track.availability_status, "audio_url": track.audio_url, "playable": bool(track.audio_url)}
