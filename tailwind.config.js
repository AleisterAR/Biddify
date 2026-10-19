/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  // List form files explicitly: a root-level glob like './*/forms.py' makes webpack watch the
  // whole project (including public/), so every build triggers another one.
  content: ['./resources/views/**/*.{js,html}', './resources/js/**/*.js', './bid/forms.py', './shipping/forms.py', './participants/forms.py', "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      colors: {
        // Saleroom palette: catalogue paper, printer's ink, brass fittings.
        // Status hues are reserved: baize green = open/leading, burnt orange = last hour,
        // red = outbid and the final minute only. Every text pair below clears 4.5:1.
        canvas: '#F6F1E7',                                        // page: catalogue paper
        card: '#FFFDF8',                                          // tags, inputs, menus: fresh card stock
        surface: { DEFAULT: '#1E1B16', raised: '#2E2922' },       // footer, auth aside (dark bands)
        onaccent: '#FFFDF8',                                      // text on ink/green buttons
        ink: { DEFAULT: '#1E1B16', soft: '#4A443B', faint: '#6B6356' },  // foreground text
        gallery: { DEFAULT: '#EAE2D0', deep: '#DDD1BA' },         // muted bands, chips, image wells
        paddle: { DEFAULT: '#1E1B16', dark: '#3A332A', light: '#F2E9D3' },     // primary action: ink
        brass: { DEFAULT: '#B08D57', dark: '#7A5C24', light: '#F3E7C9' },      // eyelets, lot numbers, focus
        live: '#2F9E62',                                          // pulsing "open for bidding" dot
        leading: { DEFAULT: '#1F5E3F', light: '#E3EEE5' },       // baize green: you're winning
        outbid: { DEFAULT: '#B42318', light: '#F8E3DE' },
        closing: { DEFAULT: '#A3410F', light: '#F7E6D6' },
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
          '0%': { backgroundColor: '#F3E7C9', transform: 'scale(1.04)' },
          '100%': { backgroundColor: 'transparent', transform: 'scale(1)' },
        },
        // The hammer falls: the hanging bid panel jolts once, then a rubber stamp lands on it
        'hammer-jolt': {
          '0%': { transform: 'rotate(0deg)' },
          '18%': { transform: 'rotate(-2.4deg)' },
          '45%': { transform: 'rotate(1.2deg)' },
          '70%': { transform: 'rotate(-.5deg)' },
          '100%': { transform: 'rotate(0deg)' },
        },
        'stamp': {
          '0%': { opacity: '0', transform: 'rotate(-8deg) scale(1.8)' },
          '60%': { opacity: '1', transform: 'rotate(-8deg) scale(.94)' },
          '100%': { opacity: '1', transform: 'rotate(-8deg) scale(1)' },
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
        'hammer-jolt': 'hammer-jolt 900ms cubic-bezier(.36,.07,.19,.97) both',
        'stamp': 'stamp 420ms cubic-bezier(.22,1,.36,1) 180ms both',
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
