import { Music, Play } from 'lucide-react'
import { Track } from '@/types/api'
import { usePlayer } from '@/context/player'

interface TrackCardProps {
  track: Track
  size?: 'small' | 'medium' | 'large'
}

export function TrackCard({ track, size = 'medium' }: TrackCardProps) {
  const { play } = usePlayer()
  const sizes = {
    small: 'w-32',
    medium: 'w-40',
    large: 'w-48',
  }

  return (
    <div
      className={`${sizes[size]} group cursor-pointer`}
      onClick={() => play(track)}
    >
      <div className="relative mb-3 overflow-hidden rounded-lg aspect-square bg-sonora-elevated">
        {track.artwork_url ? (
          <img
            src={track.artwork_url}
            alt={track.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Music className="w-16 h-16 text-sonora-text-secondary" />
          </div>
        )}
        <button className="absolute bottom-2 right-2 p-3 bg-sonora-primary text-black rounded-full opacity-0 group-hover:opacity-100 transition-opacity shadow-lg hover:bg-sonora-secondary">
          <Play className="w-5 h-5 fill-current" />
        </button>
      </div>
      <h3 className="font-semibold text-sonora-text truncate text-sm">{track.title}</h3>
      <p className="text-xs text-sonora-text-secondary truncate">Unknown Artist</p>
    </div>
  )
}
