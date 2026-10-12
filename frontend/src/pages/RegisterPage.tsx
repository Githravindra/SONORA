import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/auth'
import { Mail, Lock, User, AlertCircle, Loader } from 'lucide-react'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register, isLoading } = useAuth()
  const [formData, setFormData] = useState({ email: '', username: '', password: '' })
  const [error, setError] = useState('')
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    setValidationErrors({})
  }, [formData])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const validateForm = () => {
    const errors: Record<string, string> = {}
    if (!formData.email) errors.email = 'Email is required'
    if (!formData.email.includes('@')) errors.email = 'Invalid email'
    if (!formData.username) errors.username = 'Username is required'
    if (formData.username.length < 3) errors.username = 'Username must be at least 3 characters'
    if (!formData.password) errors.password = 'Password is required'
    if (formData.password.length < 6) errors.password = 'Password must be at least 6 characters'
    return errors
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const errors = validateForm()
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors)
      return
    }

    try {
      await register(formData.email, formData.username, formData.password)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sonora-bg to-sonora-sidebar flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-sonora-card rounded-2xl p-8 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-black text-sonora-primary mb-2">SONORA</h1>
            <p className="text-sonora-text-secondary">Create your account</p>
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
                  className={`w-full bg-sonora-elevated text-sonora-text pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-sonora-primary ${
                    validationErrors.email ? 'ring-2 ring-red-500' : ''
                  }`}
                  placeholder="you@example.com"
                />
              </div>
              {validationErrors.email && <p className="text-red-400 text-sm mt-1">{validationErrors.email}</p>}
            </div>

            <div>
              <label className="block text-sonora-text-secondary text-sm mb-2">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-3 w-5 h-5 text-sonora-text-secondary" />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className={`w-full bg-sonora-elevated text-sonora-text pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-sonora-primary ${
                    validationErrors.username ? 'ring-2 ring-red-500' : ''
                  }`}
                  placeholder="musiclover"
                />
              </div>
              {validationErrors.username && <p className="text-red-400 text-sm mt-1">{validationErrors.username}</p>}
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
                  className={`w-full bg-sonora-elevated text-sonora-text pl-10 pr-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-sonora-primary ${
                    validationErrors.password ? 'ring-2 ring-red-500' : ''
                  }`}
                  placeholder="••••••••"
                />
              </div>
              {validationErrors.password && <p className="text-red-400 text-sm mt-1">{validationErrors.password}</p>}
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary flex items-center justify-center gap-2 py-3 font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed mt-6"
            >
              {isLoading ? <Loader className="w-5 h-5 animate-spin" /> : null}
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-center text-sonora-text-secondary mt-6">
            Already have an account?{' '}
            <a href="/login" className="text-sonora-primary font-semibold hover:text-sonora-secondary transition-colors">
              Sign In
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
