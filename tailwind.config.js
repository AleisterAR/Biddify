/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./resources/views/**/*.{js,html}', "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
}

