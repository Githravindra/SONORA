import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/auth'
import { Mail, Lock, AlertCircle, Loader } from 'lucide-react'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login, isLoading } = useAuth()
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields')
      return
    }

    try {
      await login(formData.email, formData.password)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sonora-bg to-sonora-sidebar flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-sonora-card rounded-2xl p-8 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-black text-sonora-primary mb-2">SONORA</h1>
            <p className="text-sonora-text-secondary">Premium Music Streaming</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-900 bg-opacity-20 border border-red-500 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sonora-text-secondary text-sm mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-sonora-text-secondary" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-sonora-elevated text-sonora-text pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-sonora-primary"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sonora-text-secondary text-sm mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-sonora-text-secondary" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full bg-sonora-elevated text-sonora-text pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-sonora-primary"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary flex items-center justify-center gap-2 py-3 font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed mt-6"
            >
              {isLoading ? <Loader className="w-5 h-5 animate-spin" /> : null}
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-sonora-text-secondary mt-6">
            New to SONORA?{' '}
            <a href="/register" className="text-sonora-primary font-semibold hover:text-sonora-secondary transition-colors">
              Create account
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
