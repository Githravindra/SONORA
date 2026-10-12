from sqlalchemy.orm import Session

from app.db.models import User
from app.services.auth_service import AuthService


def make_demo_users(db: Session) -> None:
    from app.core.security import get_password_hash

    if db.query(User).count() == 0:
        db.add(User(email="demo@sonora.app", username="demo", password_hash=get_password_hash("demo123")))
        db.commit()


def seed_demo_catalog(db: Session) -> None:
    from app.db.models import Album, Artist, Genre, Track

    if db.query(Artist).count() == 0:
        artist = Artist(name="Luna Echo", image_url="https://example.com/luna-echo.jpg", popularity=92)
        db.add(artist)
        db.flush()
        genre = Genre(name="Indie Pop", description="Warm electronic pop")
        db.add(genre)
        db.flush()
        album = Album(title="Night Bloom", artist_id=artist.id, artwork_url="https://example.com/night-bloom.jpg")
        db.add(album)
        db.flush()
        db.add(Track(
            title="Midnight Drive",
            artist_id=artist.id,
            album_id=album.id,
            genre_id=genre.id,
            duration_seconds=238,
            mood_tags="Chill,Happy",
            artwork_url="https://example.com/night-bloom.jpg",
            audio_url="https://example.com/audio/midnight-drive.mp3",
            availability_status="demo",
            is_demo=True,
        ))
        db.commit()
