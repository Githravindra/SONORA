import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import MiniPlayer from '@/components/player/MiniPlayer'
import PlayerPanel from '@/components/player/PlayerPanel'
import { useState } from 'react'

export default function Layout() {
  const [showPlayer, setShowPlayer] = useState(false)

  return (
    <div className="flex h-screen bg-sonora-bg">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col md:ml-64">
        {/* Content area */}
        <main className="flex-1 overflow-y-auto pb-20 md:pb-0">
          <Outlet />
        </main>

        {/* Player area */}
        {showPlayer ? (
          <PlayerPanel onClose={() => setShowPlayer(false)} />
        ) : (
          <MiniPlayer />
        )}
      </div>
    </div>
  )
}
