import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 10002,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:10001',
        changeOrigin: true,
        // 不重写路径，因为后端API根路径就是/api
      },
    },
  },
})
