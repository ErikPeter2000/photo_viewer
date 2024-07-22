/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['../photo_viewer/photo_viewer/templates/**/*.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    screens: {},
    extend: {
      colors: {
        'background-default': '#f5f5f5',
        'background-dark': '#e5e5e5',
        'text-default': '#333333',
        'text-light': '#666666',
        'text-dark': '#000000',
        'text-white': '#FFFFFF',
        'banner-background': '#474949',
        'banner-text': '#FFFFFF',
        'error-text': 'darkred',
        'error-background': 'lightcoral',
        'success-text': 'darkgreen',
        'success-background': 'lightgreen',
        'image-toolbar-background': '#00000088',
        'image-toolbar-text': '#FFFFFF',
        'button-background': '#99A1AA',
        'button-text': '#FFFFFF',
        'button-background-hover': '#848D96',
      },
      boxShadow: {
        'darker': '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};