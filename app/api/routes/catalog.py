from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Album, Artist, Genre, Track
from app.schemas.catalog import AlbumResponse, ArtistResponse, GenreResponse, TrackResponse

router = APIRouter(prefix="/catalog", tags=["catalog"])


def _track_to_response(track: Track) -> dict[str, Any]:
    return {
        "id": track.id,
        "title": track.title,
        "artist_id": track.artist_id,
        "album_id": track.album_id,
        "duration": track.duration_seconds,
        "genre": track.genre.name if track.genre else "Unknown",
        "mood_tags": track.mood_tags.split(",") if track.mood_tags else [],
        "artwork_url": track.artwork_url,
        "audio_url": track.audio_url,
        "release_date": track.release_date.isoformat() if track.release_date else None,
        "explicit": track.explicit,
        "availability_status": track.availability_status,
        "play_count": track.play_count,
        "created_at": track.created_at.isoformat() if track.created_at else None,
    }


@router.get("/tracks", response_model=list[dict[str, Any]])
def list_tracks(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[dict[str, Any]]:
    tracks = db.query(Track).order_by(Track.created_at.desc()).offset(offset).limit(limit).all()
    return [_track_to_response(track) for track in tracks]


@router.get("/tracks/{track_id}")
def get_track(track_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return _track_to_response(track)


@router.get("/artists")
def list_artists(db: Session = Depends(get_db), limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)) -> list[dict[str, Any]]:
    artists = db.query(Artist).order_by(Artist.created_at.desc()).offset(offset).limit(limit).all()
    return [{"id": artist.id, "name": artist.name, "image_url": artist.image_url, "popularity": artist.popularity} for artist in artists]


@router.get("/albums")
def list_albums(db: Session = Depends(get_db), limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)) -> list[dict[str, Any]]:
    albums = db.query(Album).order_by(Album.created_at.desc()).offset(offset).limit(limit).all()
    return [{"id": album.id, "title": album.title, "artist_id": album.artist_id, "artwork_url": album.artwork_url, "release_date": album.release_date.isoformat() if album.release_date else None} for album in albums]


@router.get("/genres")
def list_genres(db: Session = Depends(get_db), limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)) -> list[dict[str, Any]]:
    genres = db.query(Genre).order_by(Genre.name).offset(offset).limit(limit).all()
    return [{"id": genre.id, "name": genre.name, "description": genre.description} for genre in genres]
