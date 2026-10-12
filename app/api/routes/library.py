from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import get_password_hash
from app.db.models import LikedTrack, Playlist, PlaylistTrack, SavedAlbum, Track, User, UserPreference

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("")
def list_playlists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict[str, Any]]:
    playlists = db.query(Playlist).filter(Playlist.owner_id == current_user.id).order_by(Playlist.updated_at.desc()).all()
    return [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "cover_artwork": p.cover_artwork,
        "track_count": len(p.tracks),
        "is_public": p.is_public,
    } for p in playlists]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_playlist(
    payload: dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    name = payload.get("name")
    if not name or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist name is required")
    playlist = Playlist(owner_id=current_user.id, name=name.strip(), description=payload.get("description"), cover_artwork=payload.get("cover_artwork"))
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return {"id": playlist.id, "name": playlist.name, "description": playlist.description, "cover_artwork": playlist.cover_artwork}


@router.get("/{playlist_id}")
def get_playlist(playlist_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id).first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    tracks = [
        {"id": pt.track.id, "title": pt.track.title, "artist_id": pt.track.artist_id, "track_id": pt.track.id, "position": pt.position}
        for pt in sorted(playlist.tracks, key=lambda item: item.position)
    ]
    return {"id": playlist.id, "name": playlist.name, "description": playlist.description, "cover_artwork": playlist.cover_artwork, "tracks": tracks}


@router.patch("/{playlist_id}")
def update_playlist(playlist_id: str, payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id).first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    if "name" in payload and payload["name"]:
        playlist.name = payload["name"]
    if "description" in payload:
        playlist.description = payload["description"]
    if "cover_artwork" in payload:
        playlist.cover_artwork = payload["cover_artwork"]
    db.commit()
    return {"id": playlist.id, "name": playlist.name, "description": playlist.description, "cover_artwork": playlist.cover_artwork}


@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id).first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    db.delete(playlist)
    db.commit()
    return {"status": "deleted", "playlist_id": playlist_id}


@router.post("/{playlist_id}/tracks")
def add_track_to_playlist(playlist_id: str, payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id).first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    track_id = payload.get("track_id")
    if not track_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="track_id is required")
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    existing = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist.id, PlaylistTrack.track_id == track.id).first()
    if existing:
        return {"status": "already_present", "playlist_id": playlist.id, "track_id": track.id}

    position = len(playlist.tracks)
    item = PlaylistTrack(playlist_id=playlist.id, track_id=track.id, position=position)
    db.add(item)
    db.commit()
    return {"status": "added", "playlist_id": playlist.id, "track_id": track.id, "position": position}


@router.delete("/{playlist_id}/tracks/{track_id}")
def remove_track_from_playlist(playlist_id: str, track_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    item = db.query(PlaylistTrack).join(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id, PlaylistTrack.track_id == track_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found in playlist")
    db.delete(item)
    db.commit()
    return {"status": "removed", "playlist_id": playlist_id, "track_id": track_id}


@router.post("/{playlist_id}/duplicate")
def duplicate_playlist(playlist_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    source = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.owner_id == current_user.id).first()
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    new_playlist = Playlist(owner_id=current_user.id, name=f"{source.name} (Copy)", description=source.description, cover_artwork=source.cover_artwork)
    db.add(new_playlist)
    db.flush()
    for idx, pt in enumerate(source.tracks):
        db.add(PlaylistTrack(playlist_id=new_playlist.id, track_id=pt.track_id, position=idx))
    db.commit()
    return {"id": new_playlist.id, "name": new_playlist.name}
