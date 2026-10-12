from sqlalchemy.orm import Session

from app.db.models import Album, Artist, Genre, Track


class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def list_tracks(self, limit: int = 20, offset: int = 0):
        return self.db.query(Track).order_by(Track.created_at.desc()).offset(offset).limit(limit).all()

    def get_track_by_id(self, track_id: str):
        return self.db.query(Track).filter(Track.id == track_id).first()

    def list_artists(self, limit: int = 20, offset: int = 0):
        return self.db.query(Artist).order_by(Artist.created_at.desc()).offset(offset).limit(limit).all()

    def list_albums(self, limit: int = 20, offset: int = 0):
        return self.db.query(Album).order_by(Album.created_at.desc()).offset(offset).limit(limit).all()

    def list_genres(self, limit: int = 20, offset: int = 0):
        return self.db.query(Genre).order_by(Genre.name).offset(offset).limit(limit).all()
