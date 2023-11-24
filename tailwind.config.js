/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      maxWidth: {
        '60rem': '60rem'
      },
      minWidth: {
        '95': '95%',
      },
    },
  },
  plugins: [],
}

