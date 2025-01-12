/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./resources/views/**/*.{js,html}', "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
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

