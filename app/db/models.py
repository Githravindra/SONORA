from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(80), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="owner", cascade="all, delete-orphan")
    liked_tracks = relationship("LikedTrack", back_populates="user", cascade="all, delete-orphan")
    saved_albums = relationship("SavedAlbum", back_populates="user", cascade="all, delete-orphan")
    followed_artists = relationship("FollowedArtist", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    listening_history = relationship("ListeningHistory", back_populates="user", cascade="all, delete-orphan")
    playback_events = relationship("PlaybackEvent", back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    recommendation_feedback = relationship("RecommendationFeedback", back_populates="user", cascade="all, delete-orphan")
    pinned_playlists = relationship("PinnedPlaylist", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    display_name = Column(String(120), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    theme = Column(String(50), default="dark")
    accent = Column(String(50), default="purple")
    autoplay = Column(Boolean, default=True)
    default_landing_page = Column(String(80), default="discover")
    layout_density = Column(String(20), default="comfortable")
    reduced_motion = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tracks = relationship("Track", back_populates="genre")


class Mood(Base):
    __tablename__ = "moods"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(200), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    popularity = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    albums = relationship("Album", back_populates="artist")
    tracks = relationship("Track", back_populates="artist")
    followed_by = relationship("FollowedArtist", back_populates="artist", cascade="all, delete-orphan")


class Album(Base):
    __tablename__ = "albums"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(200), nullable=False, index=True)
    artist_id = Column(String(36), ForeignKey("artists.id"), nullable=False)
    release_date = Column(Date, nullable=True)
    artwork_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")
    saved_by = relationship("SavedAlbum", back_populates="album", cascade="all, delete-orphan")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(200), nullable=False, index=True)
    artist_id = Column(String(36), ForeignKey("artists.id"), nullable=False)
    album_id = Column(String(36), ForeignKey("albums.id"), nullable=True)
    genre_id = Column(String(36), ForeignKey("genres.id"), nullable=True)
    duration_seconds = Column(Integer, nullable=False)
    mood_tags = Column(String(255), default="")
    artwork_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    release_date = Column(Date, nullable=True)
    explicit = Column(Boolean, default=False)
    availability_status = Column(String(50), default="available")
    play_count = Column(Integer, default=0)
    is_demo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    playlist_tracks = relationship("PlaylistTrack", back_populates="track", cascade="all, delete-orphan")
    liked_by = relationship("LikedTrack", back_populates="track", cascade="all, delete-orphan")
    listening_history = relationship("ListeningHistory", back_populates="track", cascade="all, delete-orphan")


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(180), nullable=False)
    description = Column(Text, nullable=True)
    cover_artwork = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="playlists")
    tracks = relationship("PlaylistTrack", back_populates="playlist", cascade="all, delete-orphan")
    pinned_by = relationship("PinnedPlaylist", back_populates="playlist", cascade="all, delete-orphan")


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"
    __table_args__ = (UniqueConstraint("playlist_id", "track_id", name="uq_playlist_track"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    playlist_id = Column(String(36), ForeignKey("playlists.id"), nullable=False)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    added_at = Column(DateTime, default=datetime.utcnow)

    playlist = relationship("Playlist", back_populates="tracks")
    track = relationship("Track", back_populates="playlist_tracks")


class LikedTrack(Base):
    __tablename__ = "liked_tracks"
    __table_args__ = (UniqueConstraint("user_id", "track_id", name="uq_user_liked_track"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="liked_tracks")
    track = relationship("Track", back_populates="liked_by")


class SavedAlbum(Base):
    __tablename__ = "saved_albums"
    __table_args__ = (UniqueConstraint("user_id", "album_id", name="uq_user_saved_album"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    album_id = Column(String(36), ForeignKey("albums.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_albums")
    album = relationship("Album", back_populates="saved_by")


class FollowedArtist(Base):
    __tablename__ = "followed_artists"
    __table_args__ = (UniqueConstraint("user_id", "artist_id", name="uq_user_followed_artist"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    artist_id = Column(String(36), ForeignKey("artists.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="followed_artists")
    artist = relationship("Artist", back_populates="followed_by")


class ListeningHistory(Base):
    __tablename__ = "listening_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer, default=0)
    completion_ratio = Column(Integer, default=0)

    user = relationship("User", back_populates="listening_history")
    track = relationship("Track", back_populates="listening_history")


class PlaybackEvent(Base):
    __tablename__ = "playback_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    position_seconds = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="playback_events")


class UserPreference(Base):
    __tablename__ = "user_preferences"
    __table_args__ = (UniqueConstraint("user_id", "key", name="uq_user_pref_key"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    key = Column(String(120), nullable=False)
    value = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    query = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_history")


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False)
    feedback = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendation_feedback")


class PinnedPlaylist(Base):
    __tablename__ = "pinned_playlists"
    __table_args__ = (UniqueConstraint("user_id", "playlist_id", name="uq_user_pinned_playlist"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    playlist_id = Column(String(36), ForeignKey("playlists.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="pinned_playlists")
    playlist = relationship("Playlist", back_populates="pinned_by")
