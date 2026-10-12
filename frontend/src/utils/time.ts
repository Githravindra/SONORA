export function formatTime(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '0:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  const parts = [`${minutes}:${secs.toString().padStart(2, '0')}`]
  if (hours > 0) {
    parts.unshift(`${hours}:`)
  }
  return parts.join('')
}

export function formatDuration(seconds: number): string {
  return formatTime(seconds)
}

export function formatNumber(num: number): string {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}
