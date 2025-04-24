/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          DEFAULT: 'rgb(var(--primary-rgb) / 1)',
          'dark': 'rgb(var(--primary-dark-rgb) / 1)',
          'light': 'rgb(var(--primary-light-rgb) / 1)',
          50: '#F3EFFB',
          100: '#E7DFF8',
          200: '#D0BFF0',
          300: '#B89FE9',
          400: '#917FE1',
          500: '#6A38EB',
          600: '#552CCB',
          700: '#4121A6',
          800: '#2D1782',
          900: '#190D5D',
        },
        'secondary': {
          DEFAULT: 'rgb(var(--secondary-rgb) / 1)',
          'dark': 'rgb(var(--secondary-dark-rgb) / 1)',
          'light': 'rgb(var(--secondary-light-rgb) / 1)',
          50: '#EFF6FD',
          100: '#DFEDFA',
          200: '#BEDCF6',
          300: '#9DCAF1',
          400: '#7DBBED',
          500: '#55A0E8',
          600: '#4481BA',
          700: '#34628C',
          800: '#23445D',
          900: '#12222F',
        },
        'accent': {
          DEFAULT: 'rgb(var(--accent-rgb) / 1)',
          'dark': 'rgb(var(--accent-dark-rgb) / 1)',
          'light': 'rgb(var(--accent-light-rgb) / 1)',
          50: '#EEFCF8',
          100: '#DDF9F0',
          200: '#BAF3E2',
          300: '#97EDD3',
          400: '#74E8C5',
          500: '#50E3C2',
          600: '#40B69B',
          700: '#308874',
          800: '#205B4D',
          900: '#102D27',
        },
        gold: {
          DEFAULT: '#F5C94C',
          50: '#FEF9EC',
          100: '#FDF4D9',
          200: '#FAE9B3',
          300: '#F8DE8D',
          400: '#F7D368',
          500: '#F5C94C',
          600: '#C4A03C',
          700: '#93782D',
          800: '#62501E',
          900: '#31280F',
        },
        'dark': {
          '800': 'rgb(var(--dark-800-rgb) / 1)',
          '900': 'rgb(var(--dark-900-rgb) / 1)',
          '950': 'rgb(var(--dark-950-rgb) / 1)',
          50: '#F0F1F7',
          100: '#E1E3EF',
          200: '#C3C7DE',
          300: '#A5ABCE',
          400: '#878FBD',
          500: '#6973AD',
          600: '#515C8E',
          700: '#3A446E',
          900: '#0B0F33',
        },
        'success': 'rgb(var(--success-rgb) / 1)',
        'danger': 'rgb(var(--danger-rgb) / 1)',
        'warning': 'rgb(var(--warning-rgb) / 1)',
        'info': 'rgb(var(--info-rgb) / 1)',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Space Grotesk', 'sans-serif'],
      },
      animation: {
        'gradient-x': 'gradient-x 10s ease infinite',
        'float': 'float 4s ease-in-out infinite',
      },
      keyframes: {
        'gradient-x': {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      },
    },
  },
  plugins: [],
} 