import { Music } from 'lucide-react'
import { Track } from '@/types/api'
import { formatTime } from '@/utils/time'
import { usePlayer } from '@/context/player'

interface TrackRowProps {
  track: Track
  index: number
  isCurrentTrack?: boolean
  isPlaying?: boolean
}

export function TrackRow({ track, index, isCurrentTrack, isPlaying }: TrackRowProps) {
  const { play } = usePlayer()

  return (
    <div
      onClick={() => play(track)}
      className={`group flex items-center gap-4 p-3 rounded-lg transition-colors cursor-pointer ${
        isCurrentTrack ? 'bg-sonora-elevated' : 'hover:bg-sonora-card'
      }`}
    >
      {/* Index */}
      <div className="w-8 text-center">
        {isCurrentTrack && isPlaying ? (
          <div className="flex gap-1 justify-center">
            <div className="w-1 h-3 bg-sonora-primary rounded-full animate-pulse" />
            <div className="w-1 h-2 bg-sonora-primary rounded-full animate-pulse" />
          </div>
        ) : (
          <span className="text-sm text-sonora-text-secondary group-hover:hidden">{index + 1}</span>
        )}
      </div>

      {/* Artwork */}
      {track.artwork_url && (
        <img
          src={track.artwork_url}
          alt={track.title}
          className="w-10 h-10 rounded object-cover flex-shrink-0"
        />
      )}
      {!track.artwork_url && (
        <div className="w-10 h-10 rounded bg-sonora-elevated flex items-center justify-center flex-shrink-0">
          <Music className="w-5 h-5 text-sonora-text-secondary" />
        </div>
      )}

      {/* Title and artist */}
      <div className="flex-1 min-w-0">
        <p className="text-sonora-text font-semibold truncate">{track.title}</p>
        <p className="text-sm text-sonora-text-secondary truncate">Unknown Artist</p>
      </div>

      {/* Duration */}
      <div className="w-12 text-right text-sm text-sonora-text-secondary">{formatTime(track.duration)}</div>
    </div>
  )
}
