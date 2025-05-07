import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'three': path.resolve(__dirname, 'node_modules/three'),
      'd3': path.resolve(__dirname, 'node_modules/d3'),
      'd3-3d': path.resolve(__dirname, 'node_modules/d3-3d'),
    },
  },
  optimizeDeps: {
    include: ['three', 'three/examples/jsm/controls/OrbitControls.js', 'd3', 'd3-3d'],
  },
  server: {
    port: 3001
  }
}) 