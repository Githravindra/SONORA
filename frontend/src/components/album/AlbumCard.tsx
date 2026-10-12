import { Music } from 'lucide-react'
import { Album } from '@/types/api'

interface AlbumCardProps {
  album: Album
  size?: 'small' | 'medium' | 'large'
}

export function AlbumCard({ album, size = 'medium' }: AlbumCardProps) {
  const sizes = {
    small: 'w-32',
    medium: 'w-40',
    large: 'w-48',
  }

  return (
    <div className={`${sizes[size]} group cursor-pointer`}>
      <div className="relative mb-3 overflow-hidden rounded-lg aspect-square bg-sonora-elevated">
        {album.artwork_url ? (
          <img
            src={album.artwork_url}
            alt={album.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Music className="w-16 h-16 text-sonora-text-secondary" />
          </div>
        )}
      </div>
      <h3 className="font-semibold text-sonora-text truncate text-sm">{album.title}</h3>
      <p className="text-xs text-sonora-text-secondary truncate">Unknown Artist</p>
    </div>
  )
}
