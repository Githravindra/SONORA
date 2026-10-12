export interface Track {
  id: string
  title: string
  artist_id: string
  album_id?: string | null
  duration: number
  genre?: string | null
  mood_tags?: string[]
  artwork_url?: string | null
  audio_url?: string | null
  release_date?: string | null
  explicit: boolean
  availability_status: string
  play_count: number
  created_at?: string | null
}

export interface Artist {
  id: string
  name: string
  image_url?: string | null
  popularity: number
}

export interface Album {
  id: string
  title: string
  artist_id: string
  artwork_url?: string | null
  release_date?: string | null
}

export interface Genre {
  id: string
  name: string
  description?: string | null
}

export interface Playlist {
  id: string
  name: string
  description?: string | null
  cover_artwork?: string | null
  track_count: number
  is_public: boolean
}

export interface PlaylistDetail extends Playlist {
  tracks: PlaylistTrack[]
}

export interface PlaylistTrack {
  id: string
  title: string
  artist_id: string
  track_id: string
  position: number
}

export interface User {
  id: string
  email: string
  username: string
  profile: {
    display_name: string
    theme: string
    accent: string
    autoplay: boolean
  }
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface SearchResults {
  tracks: Track[]
  artists: Artist[]
  albums: Album[]
  playlists: Playlist[]
  total: number
}

export interface PlaybackHistory {
  id: string
  track_id: string
  title?: string | null
  played_at: string
  duration_seconds: number
}

export interface AnalyticsOverview {
  total_listens: number
  total_minutes: number
}

export interface TopTrack {
  track_id: string
  title: string
  plays: number
}

export interface UserSettings {
  theme: string
  accent: string
  autoplay: boolean
  default_landing_page: string
  layout_density: string
  reduced_motion: boolean
  preferences: Record<string, string>
}
