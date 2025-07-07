import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import path from 'path'

export default defineConfig({
  base: './',
  plugins: [react(), viteSingleFile()],
  build: {
    outDir: '../media', // <- dossier que l'extension lit
    emptyOutDir: true,
    target: 'esnext',
    assetsInlineLimit: 100_000_000, // très grand pour tout inline
    rollupOptions: {
      input: path.resolve(__dirname, 'index.html'),
    },
  },
})
