import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Repeat, Repeat1, Shuffle } from 'lucide-react'
import { usePlayer } from '@/context/player'
import { formatTime } from '@/utils/time'

export default function PlayerControls() {
  const {
    isPlaying,
    currentTime,
    duration,
    volume,
    isMuted,
    shuffle,
    repeat,
    togglePlayPause,
    seek,
    previousTrack,
    nextTrack,
    setVolume,
    toggleMute,
    toggleShuffle,
    cycleRepeat,
  } = usePlayer()

  const handleProgressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    seek(parseFloat(e.target.value))
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVolume(parseFloat(e.target.value))
  }

  return (
    <div className="space-y-4">
      {/* Progress bar */}
      <div className="space-y-2">
        <input
          type="range"
          min="0"
          max={duration || 0}
          value={currentTime}
          onChange={handleProgressChange}
          className="w-full h-1 bg-sonora-elevated rounded-lg appearance-none cursor-pointer accent-sonora-primary"
        />
        <div className="flex justify-between text-xs text-sonora-text-secondary">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between">
        {/* Left controls */}
        <div className="flex items-center gap-4">
          <button
            onClick={toggleShuffle}
            className={`p-2 rounded-lg transition-colors ${
              shuffle ? 'bg-sonora-primary text-black' : 'text-sonora-text-secondary hover:text-sonora-text'
            }`}
            title="Shuffle"
          >
            <Shuffle className="w-4 h-4" />
          </button>
          <button
            onClick={previousTrack}
            className="p-2 rounded-lg text-sonora-text-secondary hover:text-sonora-text transition-colors"
            title="Previous"
          >
            <SkipBack className="w-4 h-4" />
          </button>
        </div>

        {/* Center play/pause */}
        <button
          onClick={togglePlayPause}
          className="p-3 bg-sonora-primary text-black rounded-full hover:bg-sonora-secondary transition-colors"
          title={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
        </button>

        {/* Right controls */}
        <div className="flex items-center gap-4">
          <button
            onClick={nextTrack}
            className="p-2 rounded-lg text-sonora-text-secondary hover:text-sonora-text transition-colors"
            title="Next"
          >
            <SkipForward className="w-4 h-4" />
          </button>
          <button
            onClick={cycleRepeat}
            className={`p-2 rounded-lg transition-colors ${
              repeat !== 'off' ? 'bg-sonora-primary text-black' : 'text-sonora-text-secondary hover:text-sonora-text'
            }`}
            title={`Repeat: ${repeat}`}
          >
            {repeat === 'one' ? <Repeat1 className="w-4 h-4" /> : <Repeat className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Volume */}
      <div className="flex items-center gap-3">
        <button
          onClick={toggleMute}
          className="p-1 text-sonora-text-secondary hover:text-sonora-text transition-colors"
          title={isMuted ? 'Unmute' : 'Mute'}
        >
          {isMuted || volume === 0 ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
        </button>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={volume}
          onChange={handleVolumeChange}
          className="w-24 h-1 bg-sonora-elevated rounded-lg appearance-none cursor-pointer accent-sonora-primary"
        />
      </div>
    </div>
  )
}
