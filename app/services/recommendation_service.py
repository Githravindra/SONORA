from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models import Artist, Playlist, Track


class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search(self, query: str, limit: int = 20, result_type: str | None = None):
        term = f"%{query.strip()}%"
        results = {"tracks": [], "artists": [], "playlists": []}

        if result_type in (None, "track"):
            results["tracks"] = self.db.query(Track).filter(or_(Track.title.ilike(term), Track.mood_tags.ilike(term))).limit(limit).all()
        if result_type in (None, "artist"):
            results["artists"] = self.db.query(Artist).filter(Artist.name.ilike(term)).limit(limit).all()
        if result_type in (None, "playlist"):
            results["playlists"] = self.db.query(Playlist).filter(Playlist.name.ilike(term)).limit(limit).all()
        return results
