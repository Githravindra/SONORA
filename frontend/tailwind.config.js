/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        sonora: {
          bg: '#09090B',
          sidebar: '#101012',
          card: '#18181B',
          elevated: '#222226',
          primary: '#1ED760',
          secondary: '#B8FF6A',
          text: '#FAFAFA',
          'text-secondary': '#A1A1AA',
        },
      },
      animation: {
        'pulse-subtle': 'pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'pulse-subtle': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
      },
    },
  },
  plugins: [],
}
