/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  // List form files explicitly: a root-level glob like './*/forms.py' makes webpack watch the
  // whole project (including public/), so every build triggers another one.
  content: ['./resources/views/**/*.{js,html}', './resources/js/**/*.js', './bid/forms.py', './shipping/forms.py', "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      colors: {
        // Saleroom palette
        ink: { DEFAULT: '#1A1D3A', soft: '#4A4E6E', faint: '#8A8DA6' },
        gallery: { DEFAULT: '#EEF0F4', deep: '#E1E4EC' },
        paddle: { DEFAULT: '#3340D6', dark: '#2630AE', light: '#E8EAFD' },
        brass: { DEFAULT: '#C9962B', dark: '#8C6512', light: '#F6ECD5' },
        leading: { DEFAULT: '#13804B', light: '#E3F4EA' },
        outbid: { DEFAULT: '#C2341B', light: '#FBE7E3' },
        closing: { DEFAULT: '#B45309', light: '#FEF3C7' },
      },
      fontFamily: {
        sans: ['"Instrument Sans"', ...defaultTheme.fontFamily.sans],
        display: ['"Bodoni Moda"', 'Didot', 'Georgia', 'serif'],
      },
      keyframes: {
        'tag-swing': {
          '0%': { transform: 'rotate(-9deg)' },
          '35%': { transform: 'rotate(5deg)' },
          '60%': { transform: 'rotate(-2.5deg)' },
          '80%': { transform: 'rotate(1deg)' },
          '100%': { transform: 'rotate(0deg)' },
        },
        'bid-flash': {
          '0%': { backgroundColor: '#F6ECD5', transform: 'scale(1.04)' },
          '100%': { backgroundColor: 'transparent', transform: 'scale(1)' },
        },
        'row-in': {
          '0%': { opacity: '0', transform: 'translateY(-6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'live-ping': {
          '0%': { transform: 'scale(1)', opacity: '0.7' },
          '100%': { transform: 'scale(2.4)', opacity: '0' },
        },
      },
      animation: {
        'tag-swing': 'tag-swing 1.6s cubic-bezier(.36,.07,.19,.97) both',
        'bid-flash': 'bid-flash 1.2s ease-out',
        'row-in': 'row-in 400ms ease-out both',
        'live-ping': 'live-ping 1.6s cubic-bezier(0,0,.2,1) infinite',
      },
    },
  },
  daisyui: {
    themes: ["light"],
  },
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/line-clamp'),
    require('daisyui'),
  ],
}
