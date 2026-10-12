from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import ListeningHistory, Track


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def overview_for_user(self, user_id: str):
        total_listens = self.db.query(ListeningHistory).filter(ListeningHistory.user_id == user_id).count()
        total_minutes = self.db.query(func.coalesce(func.sum(ListeningHistory.duration_seconds), 0)).filter(ListeningHistory.user_id == user_id).scalar() or 0
        return {"total_listens": total_listens, "total_minutes": int(total_minutes / 60)}

    def top_tracks(self, user_id: str, limit: int = 10):
        rows = (
            self.db.query(ListeningHistory.track_id, func.count(ListeningHistory.id).label("plays"))
            .filter(ListeningHistory.user_id == user_id)
            .group_by(ListeningHistory.track_id)
            .order_by(func.count(ListeningHistory.id).desc())
            .limit(limit)
            .all()
        )
        items = []
        for track_id, plays in rows:
            track = self.db.query(Track).filter(Track.id == track_id).first()
            if track:
                items.append({"track_id": track_id, "title": track.title, "plays": plays})
        return items
