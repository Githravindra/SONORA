from sqlalchemy.orm import Session

from app.db.models import LikedTrack, ListeningHistory, Track, UserPreference


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def personalized_recommendations(self, user_id: str, limit: int = 10):
        liked = [item.track_id for item in self.db.query(LikedTrack).filter(LikedTrack.user_id == user_id).all()]
        history = [item.track_id for item in self.db.query(ListeningHistory).filter(ListeningHistory.user_id == user_id).order_by(ListeningHistory.played_at.desc()).limit(10).all()]
        preferred_genres = [item.value for item in self.db.query(UserPreference).filter(UserPreference.user_id == user_id, UserPreference.key == "favorite_genre").all()]

        tracks = self.db.query(Track).filter(Track.id.notin_(liked + history)).limit(limit).all()
        items = []
        for track in tracks:
            genre_name = track.genre.name if track.genre else ""
            if preferred_genres and genre_name in preferred_genres:
                weight = 1.2
            else:
                weight = 1.0
            items.append({"id": track.id, "title": track.title, "genre": genre_name, "score": weight})
        return sorted(items, key=lambda item: item["score"], reverse=True)[:limit]
