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
        'banner-background': '#474949f0',
        'banner-text': '#FFFFFF',
        'error-text': 'darkred',
        'error-background': 'lightcoral',
        'success-text': 'darkgreen',
        'success-background': 'lightgreen',
        'image-toolbar-background': '#00000088',
        'image-toolbar-text': '#FFFFFF',
        'button-background': '#8A9097',
        'button-text': '#FFFFFF',
        'button-background-hover': '#70777E',
        'footer-background': '#595C5CF0',
        'footer-text': '#FAFAFA',
        'footer-text-secondary': '#E6E6E6',
      },
      boxShadow: {
        'darker': '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
      fontFamily: {
        'default': ['comic sans ms', 'sans-serif'],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};