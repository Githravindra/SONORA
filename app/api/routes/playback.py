from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Artist, Playlist, SearchHistory, Track, User

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(
    q: str = Query(..., min_length=1),
    result_type: str | None = None,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
) -> dict[str, Any]:
    if current_user:
        db.add(SearchHistory(user_id=current_user.id, query=q.strip()))
        db.commit()

    query = f"%{q.strip()}%"
    results: dict[str, Any] = {"tracks": [], "artists": [], "albums": [], "playlists": [], "total": 0}

    if result_type in (None, "track"):
        tracks = db.query(Track).filter(or_(Track.title.ilike(query), Track.mood_tags.ilike(query))).offset(offset).limit(limit).all()
        results["tracks"] = [{"id": t.id, "title": t.title, "artist_id": t.artist_id, "album_id": t.album_id, "duration": t.duration_seconds} for t in tracks]
    if result_type in (None, "artist"):
        artists = db.query(Artist).filter(Artist.name.ilike(query)).offset(offset).limit(limit).all()
        results["artists"] = [{"id": a.id, "name": a.name, "image_url": a.image_url} for a in artists]
    if result_type in (None, "playlist"):
        playlists = db.query(Playlist).filter(Playlist.name.ilike(query)).offset(offset).limit(limit).all()
        results["playlists"] = [{"id": p.id, "name": p.name, "owner_id": p.owner_id} for p in playlists]

    results["total"] = len(results["tracks"]) + len(results["artists"]) + len(results["playlists"])
    return results


@router.get("/suggestions")
def search_suggestions(q: str = Query(..., min_length=1), db: Session = Depends(get_db)) -> list[str]:
    query = f"%{q.strip()}%"
    tracks = db.query(Track.title).filter(Track.title.ilike(query)).limit(5).all()
    return [item[0] for item in tracks]


@router.get("/history")
def search_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[str]:
    rows = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).order_by(SearchHistory.created_at.desc()).limit(10).all()
    return [row.query for row in rows]


@router.delete("/history")
def clear_search_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).delete()
    db.commit()
    return {"status": "cleared"}
