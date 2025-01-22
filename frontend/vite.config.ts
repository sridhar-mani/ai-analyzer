import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import {VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Sherlock Holmes',
        short_name: 'WebLLM',
        description: 'WebLLM in a PWA',
        theme_color: '#ffffff',
        icons: [
          {
            src: '/icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
        ],
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: ({ request }) => request.destination === 'document',
            handler: 'NetworkFirst', 
            options: {
              cacheName: 'html-cache',
              expiration: { maxEntries: 10 },
            },
          },
          {
            urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: {
              cacheName: 'image-cache',
              expiration: { maxEntries: 50 },
            },
          },
          {
            urlPattern: /^https:\/\/huggingface\.co\/.*/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'huggingface-models',
              expiration: {
                maxEntries: 10,
              },
            },
          },
          {
            urlPattern: /\/models\//, 
            handler: 'CacheFirst',
            options: {
              cacheName: 'local-models',
              expiration: {
                maxEntries: 20
              },
            },
          },
        ],
      },
    }),
  ],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
});
