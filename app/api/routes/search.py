from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Album, Artist, LikedTrack, SavedAlbum, User, UserPreference,

router = APIRouter(prefix="/library", tags=["library"])


@router.get("/liked-tracks")
def get_liked_tracks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict[str, Any]]:
    rows = db.query(LikedTrack).filter(LikedTrack.user_id == current_user.id).all()
    return [{"id": row.track_id, "title": row.track.title, "artist_id": row.track.artist_id} for row in rows if row.track]


@router.post("/liked-tracks/{track_id}")
def like_track(track_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    existing = db.query(LikedTrack).filter(LikedTrack.user_id == current_user.id, LikedTrack.track_id == track_id).first()
    if existing:
        return {"status": "already_liked", "track_id": track_id}
    item = LikedTrack(user_id=current_user.id, track_id=track_id)
    db.add(item)
    db.commit()
    return {"status": "liked", "track_id": track_id}


@router.delete("/liked-tracks/{track_id}")
def unlike_track(track_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    row = db.query(LikedTrack).filter(LikedTrack.user_id == current_user.id, LikedTrack.track_id == track_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    db.delete(row)
    db.commit()
    return {"status": "removed", "track_id": track_id}


@router.get("/saved-albums")
def get_saved_albums(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict[str, Any]]:
    rows = db.query(SavedAlbum).filter(SavedAlbum.user_id == current_user.id).all()
    return [{"id": row.album_id, "title": row.album.title, "artist_id": row.album.artist_id} for row in rows if row.album]


@router.get("/followed-artists")
def get_followed_artists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict[str, Any]]:
    return [{"id": row.artist_id, "name": row.artist.name} for row in db.query(FollowedArtist).filter(FollowedArtist.user_id == current_user.id).all() if row.artist]


@router.get("")
def get_library(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    liked = get_liked_tracks(db=db, current_user=current_user)
    saved = get_saved_albums(db=db, current_user=current_user)
    followed = get_followed_artists(db=db, current_user=current_user)
    return {"liked_tracks": liked, "saved_albums": saved, "followed_artists": followed}
