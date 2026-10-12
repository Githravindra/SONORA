import { Playlist as PlaylistIcon } from 'lucide-react'
import { Playlist } from '@/types/api'

interface PlaylistCardProps {
  playlist: Playlist
  size?: 'small' | 'medium' | 'large'
}

export function PlaylistCard({ playlist, size = 'medium' }: PlaylistCardProps) {
  const sizes = {
    small: 'w-32',
    medium: 'w-40',
    large: 'w-48',
  }

  return (
    <div className={`${sizes[size]} group cursor-pointer`}>
      <div className="relative mb-3 overflow-hidden rounded-lg aspect-square bg-gradient-to-br from-sonora-primary to-sonora-secondary">
        {playlist.cover_artwork ? (
          <img
            src={playlist.cover_artwork}
            alt={playlist.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <PlaylistIcon className="w-16 h-16 text-black opacity-50" />
          </div>
        )}
      </div>
      <h3 className="font-semibold text-sonora-text truncate text-sm">{playlist.name}</h3>
      <p className="text-xs text-sonora-text-secondary">{playlist.track_count} songs</p>
    </div>
  )
}
