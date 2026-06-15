/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tickle: {
          bg: '#0c0c14',
          raised: '#13131f',
          card: '#191928',
          cardHover: '#1f1f34',
          border: '#262640',
          accent: '#ff6b6b',
          accentHover: '#ff5252',
          secondary: '#feca57',
          cool: '#48dbfb',
          text: '#e2e2ee',
          muted: '#8888a8'
        }
      },
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        display: ['Silkscreen', 'cursive'],
        mono: ['DM Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
