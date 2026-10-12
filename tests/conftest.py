from typing import Any


class MediaService:
    def __init__(self, backend: str = "local"):
        self.backend = backend

    def resolve_audio_url(self, track_data: dict[str, Any]) -> str | None:
        if track_data.get("audio_url"):
            return track_data["audio_url"]
        return None

    def can_stream(self, track_data: dict[str, Any]) -> bool:
        return bool(track_data.get("audio_url"))
