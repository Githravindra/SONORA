from pydantic import BaseModel


class TrackResponse(BaseModel):
    id: str
    title: str
    artist_id: str | None = None
    album_id: str | None = None
    duration: int
    genre: str | None = None
    mood_tags: list[str] = []
    artwork_url: str | None = None
    audio_url: str | None = None
    release_date: str | None = None
    explicit: bool = False
    availability_status: str = "available"
    play_count: int = 0
