import { X, Maximize2 } from 'lucide-react'
import { usePlayer } from '@/context/player'
import PlayerControls from './PlayerControls'
import { useState } from 'react'

export default function PlayerPanel({ onClose }: { onClose?: () => void }) {
  const { currentTrack } = usePlayer()
  const [view, setView] = useState<'artwork' | 'queue' | 'lyrics'>('artwork')

  return (
    <div className="fixed inset-0 bg-gradient-to-b from-sonora-card to-sonora-bg z-50 md:static md:relative md:bg-sonora-card md:border-t md:border-sonora-elevated">
      {/* Header */}
      <div className="flex items-center justify-between p-4 md:hidden">
        <h2 className="text-lg font-bold text-sonora-text">Now Playing</h2>
        {onClose && (
          <button
            onClick={onClose}
            className="p-2 text-sonora-text-secondary hover:text-sonora-text transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-col h-full p-6 space-y-6">
        {/* Artwork */}
        {view === 'artwork' && currentTrack?.artwork_url && (
          <div className="flex-1 flex items-center justify-center">
            <div className="relative">
              <img
                src={currentTrack.artwork_url}
                alt={currentTrack.title}
                className="w-64 h-64 md:w-48 md:h-48 rounded-2xl shadow-2xl object-cover"
              />
            </div>
          </div>
        )}

        {/* Track info */}
        {currentTrack && (
          <div className="text-center">
            <h3 className="text-2xl md:text-xl font-bold text-sonora-text mb-2">{currentTrack.title}</h3>
            <p className="text-sonora-text-secondary">Unknown Artist</p>
          </div>
        )}

        {/* Controls */}
        <PlayerControls />

        {/* View tabs */}
        <div className="flex gap-2 border-b border-sonora-elevated">
          {(['artwork', 'queue', 'lyrics'] as const).map((v) => (
            <button
              key={v}
              onClick={() => setView(v)}
              className={`px-4 py-2 font-semibold transition-colors capitalize ${
                view === v
                  ? 'text-sonora-primary border-b-2 border-sonora-primary'
                  : 'text-sonora-text-secondary hover:text-sonora-text'
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
