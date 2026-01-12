/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        atomic: {
          teal: 'var(--atomic-teal)',
          tangerine: 'var(--atomic-tangerine)',
          mustard: 'var(--atomic-mustard)',
          beige: 'var(--atomic-beige)',
        },
      },
    },
  },
  plugins: [],
};
