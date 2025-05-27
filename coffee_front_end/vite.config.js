import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // 添加生产环境配置
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 生成sourcemap便于调试
    sourcemap: true,
    // 使用默认的压缩方式，不指定terser
    minify: 'esbuild',
  },
  // 开发服务器配置
  server: {
    port: 5173,
    open: true,
    cors: true,
    proxy: {
      // 开发环境API代理配置
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
