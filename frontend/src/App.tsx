import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from '@/context/auth'
import { PlayerProvider } from '@/context/player'
import Layout from '@/components/layout/Layout'
import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import HomePage from '@/pages/HomePage'
import SearchPage from '@/pages/SearchPage'
import DiscoveryPage from '@/pages/DiscoveryPage'
import LibraryPage from '@/pages/LibraryPage'
import PlaylistPage from '@/pages/PlaylistPage'
import SettingsPage from '@/pages/SettingsPage'
import NowPlayingPage from '@/pages/NowPlayingPage'

function AppRoutes() {
  const { isAuthenticated, isLoading, checkAuth } = useAuth()

  useEffect(() => {
    checkAuth()
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center w-full h-screen bg-sonora-bg">
        <div className="text-sonora-text">
          <div className="animate-pulse-subtle text-2xl font-bold mb-2">SONORA</div>
          <p className="text-sonora-text-secondary">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <Routes>
      {!isAuthenticated ? (
        <>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </>
      ) : (
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/discover" element={<DiscoveryPage />} />
          <Route path="/library" element={<LibraryPage />} />
          <Route path="/playlist/:playlistId" element={<PlaylistPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/now-playing" element={<NowPlayingPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      )}
    </Routes>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <PlayerProvider>
          <AppRoutes />
        </PlayerProvider>
      </AuthProvider>
    </Router>
  )
}

export default App
