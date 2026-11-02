import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// Applied to the production build only: the dev server needs inline scripts for
// hot reload. connect-src 'none' makes any accidental network call fail loudly.
const CSP = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self'",
  "connect-src 'none'",
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
].join('; ');

const injectCsp = {
  name: 'dojo-explorer-csp',
  apply: 'build',
  transformIndexHtml(html) {
    return html.replace(
      '<!-- CSP-PLACEHOLDER -->',
      `<meta http-equiv="Content-Security-Policy" content="${CSP}" />`,
    );
  },
};

export default defineConfig({
  base: './',
  plugins: [react(), injectCsp],
  server: { host: '127.0.0.1', port: 5173, strictPort: true },
  preview: { host: '127.0.0.1', port: 4173, strictPort: true },
  build: { modulePreload: { polyfill: false } },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test-setup.js'],
    include: ['src/**/*.test.{js,jsx}'],
    exclude: ['src/v2/**/*.test.mjs', 'node_modules/**'],
    css: false,
    restoreMocks: true,
  },
});
