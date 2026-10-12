import { Artist } from '@/types/api'

interface ArtistCardProps {
  artist: Artist
  size?: 'small' | 'medium' | 'large'
}

export function ArtistCard({ artist, size = 'medium' }: ArtistCardProps) {
  const sizes = {
    small: 'w-32',
    medium: 'w-40',
    large: 'w-48',
  }

  return (
    <div className={`${sizes[size]} group cursor-pointer text-center`}>
      <div className="relative mb-3 overflow-hidden rounded-full aspect-square bg-sonora-elevated">
        {artist.image_url ? (
          <img
            src={artist.image_url}
            alt={artist.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-sonora-primary to-sonora-secondary flex items-center justify-center text-black font-bold text-4xl">
            {artist.name.charAt(0)}
          </div>
        )}
      </div>
      <h3 className="font-semibold text-sonora-text truncate text-sm">{artist.name}</h3>
      <p className="text-xs text-sonora-text-secondary">Artist</p>
    </div>
  )
}
