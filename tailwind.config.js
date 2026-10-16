/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  // List form files explicitly: a root-level glob like './*/forms.py' makes webpack watch the
  // whole project (including public/), so every build triggers another one.
  content: ['./resources/views/**/*.{js,html}', './resources/js/**/*.js', './bid/forms.py', './shipping/forms.py', "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      colors: {
        // "Professional blue + deal green" palette from ui-ux-pro-max (light)
        canvas: '#F8FAFC',                                        // page background
        card: '#FFFFFF',                                          // cards, inputs, menus
        surface: { DEFAULT: '#0F172A', raised: '#1E293B' },       // footer, side panels (dark bands)
        onaccent: '#FFFFFF',                                      // text on blue/green buttons
        ink: { DEFAULT: '#0F172A', soft: '#334155', faint: '#475569' },  // foreground text
        gallery: { DEFAULT: '#F1F5FD', deep: '#E4ECFC' },         // muted bands, chips, borders
        paddle: { DEFAULT: '#2563EB', dark: '#1D4ED8', light: '#DBEAFE' },     // primary blue
        brass: { DEFAULT: '#3B82F6', dark: '#1D4ED8', light: '#EFF6FF' },      // tag hole, lot numbers
        leading: { DEFAULT: '#047857', light: '#D1FAE5' },       // deal green, darkened from #059669 for 4.5:1 text
        outbid: { DEFAULT: '#DC2626', light: '#FEE2E2' },
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
          '0%': { backgroundColor: '#DBEAFE', transform: 'scale(1.04)' },
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
