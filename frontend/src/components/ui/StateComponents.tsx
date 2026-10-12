import { ReactNode } from 'react'
import { AlertCircle, Loader } from 'lucide-react'

export function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader className="w-8 h-8 text-sonora-primary animate-spin mb-3" />
      <p className="text-sonora-text-secondary">Loading...</p>
    </div>
  )
}

export function ErrorState({ message = 'Something went wrong' }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <AlertCircle className="w-12 h-12 text-red-500 mb-3" />
      <p className="text-sonora-text-secondary text-center max-w-md">{message}</p>
    </div>
  )
}

export function EmptyState({ message = 'No results found' }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <p className="text-sonora-text-secondary text-lg">{message}</p>
    </div>
  )
}

export function Skeleton() {
  return <div className="bg-sonora-elevated rounded animate-pulse h-full" />
}

export interface CardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
}

export function Card({ children, className = '', onClick }: CardProps) {
  return (
    <div
      className={`card cursor-pointer ${onClick ? 'hover:bg-opacity-80' : ''} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  )
}
