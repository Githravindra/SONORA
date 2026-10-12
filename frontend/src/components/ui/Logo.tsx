import { Music } from 'lucide-react'

export default function Logo() {
  return (
    <div className="flex items-center gap-2">
      <div className="w-8 h-8 bg-sonora-primary rounded-lg flex items-center justify-center">
        <Music className="w-5 h-5 text-black" />
      </div>
      <span className="font-black text-xl text-sonora-primary">SONORA</span>
    </div>
  )
}
