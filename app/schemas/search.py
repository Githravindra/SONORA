from pydantic import BaseModel


class PlaylistCreateRequest(BaseModel):
    name: str
    description: str | None = None
    cover_artwork: str | None = None
