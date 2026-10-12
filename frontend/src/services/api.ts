import axios, { AxiosInstance, AxiosError } from 'axios'
import { AuthResponse, User, Track, Artist, Album, Genre, Playlist, SearchResults, PlaybackHistory, AnalyticsOverview, TopTrack, UserSettings } from '@/types/api'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: `${BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  async register(email: string, username: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post('/auth/register', {
      email,
      username,
      password,
    })
    return response.data
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post('/auth/login', {
      email,
      password,
    })
    return response.data
  }

  async getMe(): Promise<User> {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  async getSearchHistory(): Promise<string[]> {
    const response = await this.client.get('/auth/search-history')
    return response.data
  }

  // Catalog endpoints
  async getTracks(limit: number = 20, offset: number = 0): Promise<Track[]> {
    const response = await this.client.get('/catalog/tracks', {
      params: { limit, offset },
    })
    return response.data
  }

  async getTrack(trackId: string): Promise<Track> {
    const response = await this.client.get(`/catalog/tracks/${trackId}`)
    return response.data
  }

  async getArtists(limit: number = 20, offset: number = 0): Promise<Artist[]> {
    const response = await this.client.get('/catalog/artists', {
      params: { limit, offset },
    })
    return response.data
  }

  async getAlbums(limit: number = 20, offset: number = 0): Promise<Album[]> {
    const response = await this.client.get('/catalog/albums', {
      params: { limit, offset },
    })
    return response.data
  }

  async getGenres(limit: number = 20, offset: number = 0): Promise<Genre[]> {
    const response = await this.client.get('/catalog/genres', {
      params: { limit, offset },
    })
    return response.data
  }

  // Search endpoint
  async search(
    q: string,
    resultType?: string,
    limit: number = 20,
    offset: number = 0
  ): Promise<SearchResults> {
    const response = await this.client.get('/search', {
      params: { q, result_type: resultType, limit, offset },
    })
    return response.data
  }

  async getSearchSuggestions(q: string): Promise<string[]> {
    const response = await this.client.get('/search/suggestions', {
      params: { q },
    })
    return response.data
  }

  async clearSearchHistory(): Promise<void> {
    await this.client.delete('/search/history')
  }

  // Playlists endpoints
  async getPlaylists(): Promise<Playlist[]> {
    const response = await this.client.get('/playlists')
    return response.data
  }

  async createPlaylist(name: string, description?: string, coverArtwork?: string): Promise<Playlist> {
    const response = await this.client.post('/playlists', {
      name,
      description,
      cover_artwork: coverArtwork,
    })
    return response.data
  }

  async getPlaylist(playlistId: string): Promise<any> {
    const response = await this.client.get(`/playlists/${playlistId}`)
    return response.data
  }

  async updatePlaylist(playlistId: string, data: any): Promise<Playlist> {
    const response = await this.client.patch(`/playlists/${playlistId}`, data)
    return response.data
  }

  async deletePlaylist(playlistId: string): Promise<void> {
    await this.client.delete(`/playlists/${playlistId}`)
  }

  async addTrackToPlaylist(playlistId: string, trackId: string): Promise<any> {
    const response = await this.client.post(`/playlists/${playlistId}/tracks`, {
      track_id: trackId,
    })
    return response.data
  }

  async removeTrackFromPlaylist(playlistId: string, trackId: string): Promise<void> {
    await this.client.delete(`/playlists/${playlistId}/tracks/${trackId}`)
  }

  async duplicatePlaylist(playlistId: string): Promise<Playlist> {
    const response = await this.client.post(`/playlists/${playlistId}/duplicate`)
    return response.data
  }

  // Library endpoints
  async getLikedTracks(): Promise<any[]> {
    const response = await this.client.get('/library/liked-tracks')
    return response.data
  }

  async likeTrack(trackId: string): Promise<any> {
    const response = await this.client.post(`/library/liked-tracks/${trackId}`)
    return response.data
  }

  async unlikeTrack(trackId: string): Promise<void> {
    await this.client.delete(`/library/liked-tracks/${trackId}`)
  }

  async getSavedAlbums(): Promise<any[]> {
    const response = await this.client.get('/library/saved-albums')
    return response.data
  }

  async getFollowedArtists(): Promise<any[]> {
    const response = await this.client.get('/library/followed-artists')
    return response.data
  }

  async getLibrary(): Promise<any> {
    const response = await this.client.get('/library')
    return response.data
  }

  // Playback endpoints
  async recordPlaybackStart(trackId: string): Promise<any> {
    const response = await this.client.post('/playback/start', {
      track_id: trackId,
    })
    return response.data
  }

  async recordPlaybackProgress(trackId: string, positionSeconds: number): Promise<any> {
    const response = await this.client.post('/playback/progress', {
      track_id: trackId,
      position_seconds: positionSeconds,
    })
    return response.data
  }

  async recordPlaybackComplete(trackId: string, durationSeconds: number): Promise<any> {
    const response = await this.client.post('/playback/complete', {
      track_id: trackId,
      duration_seconds: durationSeconds,
    })
    return response.data
  }

  async getPlaybackHistory(limit: number = 20): Promise<PlaybackHistory[]> {
    const response = await this.client.get('/playback/history', {
      params: { limit },
    })
    return response.data
  }

  async getQueue(): Promise<any> {
    const response = await this.client.get('/playback/queue')
    return response.data
  }

  async saveQueue(tracks: string[]): Promise<any> {
    const response = await this.client.post('/playback/queue', {
      tracks,
    })
    return response.data
  }

  async getTrackAvailability(trackId: string): Promise<any> {
    const response = await this.client.get(`/playback/availability/${trackId}`)
    return response.data
  }

  // Discovery endpoints
  async getRecommendations(limit: number = 10): Promise<Track[]> {
    const response = await this.client.get('/discovery/recommendations', {
      params: { limit },
    })
    return response.data
  }

  async getTrendingTracks(limit: number = 10): Promise<Track[]> {
    const response = await this.client.get('/discovery/trending', {
      params: { limit },
    })
    return response.data
  }

  async getSimilarTracks(trackId: string, limit: number = 5): Promise<Track[]> {
    const response = await this.client.get(`/discovery/similar/${trackId}`, {
      params: { limit },
    })
    return response.data
  }

  // Analytics endpoints
  async getAnalyticsOverview(): Promise<AnalyticsOverview> {
    const response = await this.client.get('/analytics/overview')
    return response.data
  }

  async getTopTracks(limit: number = 10): Promise<TopTrack[]> {
    const response = await this.client.get('/analytics/top-tracks', {
      params: { limit },
    })
    return response.data
  }

  // Settings endpoints
  async getSettings(): Promise<UserSettings> {
    const response = await this.client.get('/settings')
    return response.data
  }

  async updateSettings(settings: any): Promise<UserSettings> {
    const response = await this.client.put('/settings', settings)
    return response.data
  }
}

export const apiClient = new ApiClient()
