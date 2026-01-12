import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/modules': 'http://localhost:8000',
      '/proxy': 'http://localhost:8000',
    },
  },
});
