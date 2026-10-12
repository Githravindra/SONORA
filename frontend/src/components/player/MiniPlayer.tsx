import { usePlayer } from '@/context/player'
import { Heart, Music, Clock } from 'lucide-react'

export default function MiniPlayer() {
  const { currentTrack, isPlaying } = usePlayer()

  if (!currentTrack) {
    return (
      <div className="h-20 bg-sonora-card border-t border-sonora-elevated flex items-center justify-center text-sonora-text-secondary">
        <div className="flex items-center gap-2">
          <Music className="w-5 h-5" />
          <span>No track playing</span>
        </div>
      </div>
    )
  }

  return (
    <div className="h-20 bg-sonora-card border-t border-sonora-elevated px-4 flex items-center justify-between">
      <div className="flex items-center gap-3 flex-1 min-w-0">
        {currentTrack.artwork_url && (
          <img
            src={currentTrack.artwork_url}
            alt={currentTrack.title}
            className="w-14 h-14 rounded object-cover flex-shrink-0"
          />
        )}
        <div className="flex-1 min-w-0">
          <p className="text-sonora-text font-semibold truncate">{currentTrack.title}</p>
          <p className="text-sonora-text-secondary text-sm truncate">Unknown Artist</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {isPlaying && (
          <div className="flex gap-1">
            <div className="w-1 h-6 bg-sonora-primary rounded-full animate-pulse" />
            <div className="w-1 h-4 bg-sonora-primary rounded-full animate-pulse" />
            <div className="w-1 h-5 bg-sonora-primary rounded-full animate-pulse" />
          </div>
        )}
        <button className="p-2 text-sonora-text-secondary hover:text-sonora-primary transition-colors">
          <Heart className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}
