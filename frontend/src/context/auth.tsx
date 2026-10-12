import { ReactNode, createContext, useContext, useState, useCallback } from 'react'
import { User } from '@/types/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setUser(null)
      setIsLoading(false)
      return
    }

    try {
      const { apiClient } = await import('@/services/api')
      const userData = await apiClient.getMe()
      setUser(userData)
    } catch (error) {
      localStorage.removeItem('access_token')
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const { apiClient } = await import('@/services/api')
      const response = await apiClient.login(email, password)
      localStorage.setItem('access_token', response.access_token)
      const userData = await apiClient.getMe()
      setUser(userData)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const register = useCallback(async (email: string, username: string, password: string) => {
    setIsLoading(true)
    try {
      const { apiClient } = await import('@/services/api')
      const response = await apiClient.register(email, username, password)
      localStorage.setItem('access_token', response.access_token)
      const userData = await apiClient.getMe()
      setUser(userData)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        checkAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
