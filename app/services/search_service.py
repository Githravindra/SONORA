from sqlalchemy.orm import Session

from app.db.models import Playlist, PlaylistTrack, Track


class PlaylistService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: str, name: str, description: str | None = None, cover_artwork: str | None = None):
        playlist = Playlist(owner_id=user_id, name=name, description=description, cover_artwork=cover_artwork)
        self.db.add(playlist)
        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def add_track(self, playlist_id: str, track_id: str):
        existing = self.db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id).first()
        if existing:
            return existing
        position = self.db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).count()
        item = PlaylistTrack(playlist_id=playlist_id, track_id=track_id, position=position)
        self.db.add(item)
        self.db.commit()
        return item

    def remove_track(self, playlist_id: str, track_id: str):
        item = self.db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
        return True
