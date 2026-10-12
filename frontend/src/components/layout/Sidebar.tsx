import { useState } from 'react'
import { Menu, X, Home, Search, Compass, Music, Settings, Heart, Plus } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '@/context/auth'
import Logo from '@/components/ui/Logo'

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()
  const { logout, user } = useAuth()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/search', icon: Search, label: 'Search' },
    { path: '/discover', icon: Compass, label: 'Discover' },
    { path: '/library', icon: Music, label: 'Your Library' },
    { path: '/library?tab=liked', icon: Heart, label: 'Liked Songs' },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 md:hidden p-2 text-sonora-text hover:bg-sonora-card rounded-lg transition-colors"
      >
        {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-screen w-64 bg-sonora-sidebar border-r border-sonora-elevated transform transition-transform md:translate-x-0 z-40 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="h-full flex flex-col p-6">
          {/* Logo */}
          <Link to="/" className="mb-8 block">
            <Logo />
          </Link>

          {/* Main nav */}
          <nav className="flex-1 space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive(item.path)
                    ? 'bg-sonora-primary text-black font-semibold'
                    : 'text-sonora-text-secondary hover:text-sonora-text hover:bg-sonora-card'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          {/* Playlists section */}
          <div className="border-t border-sonora-elevated pt-4 mb-4">
            <button className="w-full flex items-center gap-2 px-4 py-2 text-sonora-text-secondary hover:text-sonora-text transition-colors text-sm font-semibold">
              <Plus className="w-4 h-4" />
              Create Playlist
            </button>
            <div className="mt-3 space-y-1 max-h-32 overflow-y-auto scrollbar-hide">
              {/* Placeholder for playlists */}
              <p className="text-xs text-sonora-text-secondary px-4 py-2">No playlists yet</p>
            </div>
          </div>

          {/* Footer */}
          <div className="border-t border-sonora-elevated pt-4 space-y-2">
            <Link
              to="/settings"
              className="flex items-center gap-3 px-4 py-2 text-sonora-text-secondary hover:text-sonora-text transition-colors rounded-lg hover:bg-sonora-card"
              onClick={() => setIsOpen(false)}
            >
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </Link>
            {user && (
              <button
                onClick={() => {
                  logout()
                  setIsOpen(false)
                }}
                className="w-full flex items-center justify-between px-4 py-2 text-sonora-text-secondary hover:text-sonora-text transition-colors rounded-lg hover:bg-sonora-card text-sm"
              >
                <span>Logout</span>
                <span className="text-xs font-semibold text-sonora-primary">{user.username}</span>
              </button>
            )}
          </div>
        </div>
      </aside>
    </>
  )
}
