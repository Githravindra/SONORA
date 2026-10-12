import { ReactNode, createContext, useContext, useState, useCallback, useRef, useEffect } from 'react'
import { Track } from '@/types/api'

interface PlayerContextType {
  currentTrack: Track | null
  isPlaying: boolean
  currentTime: number
  duration: number
  volume: number
  isMuted: boolean
  queue: Track[]
  queueIndex: number
  shuffle: boolean
  repeat: 'off' | 'all' | 'one'
  play: (track: Track) => void
  pause: () => void
  resume: () => void
  togglePlayPause: () => void
  seek: (time: number) => void
  setVolume: (volume: number) => void
  toggleMute: () => void
  nextTrack: () => void
  previousTrack: () => void
  toggleShuffle: () => void
  cycleRepeat: () => void
  setQueue: (tracks: Track[], startIndex?: number) => void
  addToQueue: (track: Track) => void
  removeFromQueue: (index: number) => void
}

const PlayerContext = createContext<PlayerContextType | undefined>(undefined)

export const PlayerProvider = ({ children }: { children: ReactNode }) => {
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolumeState] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [queue, setQueueState] = useState<Track[]>([])
  const [queueIndex, setQueueIndex] = useState(0)
  const [shuffle, setShuffle] = useState(false)
  const [repeat, setRepeat] = useState<'off' | 'all' | 'one'>('off')

  // Initialize audio element
  useEffect(() => {
    if (!audioRef.current) {
      audioRef.current = new Audio()
      audioRef.current.addEventListener('timeupdate', () => {
        setCurrentTime(audioRef.current?.currentTime || 0)
      })
      audioRef.current.addEventListener('loadedmetadata', () => {
        setDuration(audioRef.current?.duration || 0)
      })
      audioRef.current.addEventListener('ended', handleTrackEnd)
      audioRef.current.addEventListener('error', (e) => {
        console.error('Audio error:', e)
        setIsPlaying(false)
      })
    }
    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
        audioRef.current.src = ''
      }
    }
  }, [])

  const handleTrackEnd = useCallback(() => {
    if (repeat === 'one') {
      if (audioRef.current) {
        audioRef.current.currentTime = 0
        audioRef.current.play()
      }
    } else {
      nextTrack()
    }
  }, [repeat])

  const play = useCallback((track: Track) => {
    if (!audioRef.current) return
    
    if (!track.audio_url) {
      console.error('No audio URL available for track:', track.id)
      return
    }

    setCurrentTrack(track)
    audioRef.current.src = track.audio_url
    audioRef.current.play().catch((error) => {
      console.error('Error playing track:', error)
    })
    setIsPlaying(true)
  }, [])

  const pause = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }, [])

  const resume = useCallback(() => {
    if (audioRef.current && currentTrack) {
      audioRef.current.play().catch((error) => {
        console.error('Error resuming playback:', error)
      })
      setIsPlaying(true)
    }
  }, [currentTrack])

  const togglePlayPause = useCallback(() => {
    if (isPlaying) {
      pause()
    } else if (currentTrack) {
      resume()
    }
  }, [isPlaying, currentTrack, pause, resume])

  const seek = useCallback((time: number) => {
    if (audioRef.current) {
      audioRef.current.currentTime = time
      setCurrentTime(time)
    }
  }, [])

  const setVolume = useCallback((vol: number) => {
    const newVolume = Math.max(0, Math.min(1, vol))
    setVolumeState(newVolume)
    if (audioRef.current) {
      audioRef.current.volume = newVolume
    }
  }, [])

  const toggleMute = useCallback(() => {
    if (isMuted) {
      setVolume(volume || 0.5)
      setIsMuted(false)
    } else {
      setVolume(0)
      setIsMuted(true)
    }
  }, [isMuted, volume, setVolume])

  const nextTrack = useCallback(() => {
    if (queue.length === 0) return
    
    let nextIndex = queueIndex + 1
    if (nextIndex >= queue.length) {
      if (repeat === 'all') {
        nextIndex = 0
      } else {
        setIsPlaying(false)
        return
      }
    }
    
    setQueueIndex(nextIndex)
    play(queue[nextIndex])
  }, [queue, queueIndex, repeat, play])

  const previousTrack = useCallback(() => {
    if (queue.length === 0) return
    
    if (currentTime > 3) {
      seek(0)
    } else {
      let prevIndex = queueIndex - 1
      if (prevIndex < 0) {
        prevIndex = queue.length - 1
      }
      setQueueIndex(prevIndex)
      play(queue[prevIndex])
    }
  }, [queue, queueIndex, currentTime, seek, play])

  const toggleShuffle = useCallback(() => {
    setShuffle(!shuffle)
  }, [shuffle])

  const cycleRepeat = useCallback(() => {
    setRepeat((current) => {
      if (current === 'off') return 'all'
      if (current === 'all') return 'one'
      return 'off'
    })
  }, [])

  const setQueue = useCallback((tracks: Track[], startIndex: number = 0) => {
    setQueueState(tracks)
    setQueueIndex(startIndex)
    if (tracks.length > 0) {
      play(tracks[startIndex])
    }
  }, [play])

  const addToQueue = useCallback((track: Track) => {
    setQueueState((prev) => [...prev, track])
  }, [])

  const removeFromQueue = useCallback((index: number) => {
    setQueueState((prev) => prev.filter((_, i) => i !== index))
    if (index === queueIndex) {
      nextTrack()
    } else if (index < queueIndex) {
      setQueueIndex(queueIndex - 1)
    }
  }, [queueIndex, nextTrack])

  return (
    <PlayerContext.Provider
      value={{
        currentTrack,
        isPlaying,
        currentTime,
        duration,
        volume,
        isMuted,
        queue,
        queueIndex,
        shuffle,
        repeat,
        play,
        pause,
        resume,
        togglePlayPause,
        seek,
        setVolume,
        toggleMute,
        nextTrack,
        previousTrack,
        toggleShuffle,
        cycleRepeat,
        setQueue,
        addToQueue,
        removeFromQueue,
      }}
    >
      {children}
      <audio ref={audioRef} />
    </PlayerContext.Provider>
  )
}

export const usePlayer = () => {
  const context = useContext(PlayerContext)
  if (context === undefined) {
    throw new Error('usePlayer must be used within PlayerProvider')
  }
  return context
}
