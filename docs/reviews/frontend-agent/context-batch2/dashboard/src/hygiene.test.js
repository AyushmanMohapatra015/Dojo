import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';

// Run from the dashboard/ directory (npm test does this).
const root = process.cwd();
const read = (...parts) => readFileSync(join(root, ...parts), 'utf8');

const SOURCES = [
  'src/App.jsx',
  'src/main.jsx',
  'index.html',
  'src/styles.css',
  'src/components/ExplorerNavigation.jsx',
  'src/components/ExplorerNavigation.css',
  'src/v2/exact.mjs',
  'src/v2/data.mjs',
  'src/v2/derive.mjs',
];

const FORBIDDEN = [
  [/dangerouslySetInnerHTML/, 'dangerouslySetInnerHTML'],
  [/\beval\s*\(/, 'eval('],
  [/new\s+Function\b/, 'new Function'],
  [/\bfetch\s*\(/, 'fetch('],
  [/XMLHttpRequest/, 'XMLHttpRequest'],
  [/WebSocket/, 'WebSocket'],
  [/sendBeacon/, 'sendBeacon'],
  [/https?:\/\//, 'absolute http(s) URL'],
  [/@import/, 'CSS @import'],
  [/\bimport\s*\(/, 'dynamic import'],
  [/localStorage|sessionStorage|document\.cookie|indexedDB/, 'browser storage'],
  [/innerHTML|outerHTML|insertAdjacentHTML|document\.write/, 'raw HTML sinks'],
];

describe('source hygiene (v2)', () => {
  for (const file of SOURCES) {
    it(`${file} has no remote, dynamic-code or raw-HTML constructs`, () => {
      const text = read(...file.split('/'));
      for (const [pattern, label] of FORBIDDEN) {
        expect(pattern.test(text) ? `${file} contains${label}` : 'clean').toBe('clean');
      }
    });
  }

  it('App.jsx does not import legacy v1 data.js or synthetic.json', () => {
    const appText = read('src', 'App.jsx');
    expect(appText).not.toMatch(/\.\/data\.js/);
    expect(appText).not.toMatch(/fixtures\/synthetic\.json/);
  });

  it('declares only the documented dependency set and runs both v2 Node and UI tests', () => {
    const pkg = JSON.parse(read('package.json'));
    expect(Object.keys(pkg.dependencies).sort()).toEqual([
      'react',
      'react-dom',
      'react-is',
      'recharts',
    ]);
    expect(Object.keys(pkg.devDependencies).sort()).toEqual([
      '@testing-library/dom',
      '@testing-library/jest-dom',
      '@testing-library/react',
      '@testing-library/user-event',
      '@vitejs/plugin-react',
      'jsdom',
      'vite',
      'vitest',
    ]);
    expect(pkg.scripts['test:v2']).toMatch(/node --test/);
    expect(pkg.scripts['test:ui']).toMatch(/vitest run/);
  });

  it('binds local servers to 127.0.0.1 only', () => {
    const pkg = JSON.parse(read('package.json'));
    expect(pkg.scripts.dev).toMatch(/--host 127\.0\.0\.1/);
    expect(pkg.scripts.preview).toMatch(/--host 127\.0\.0\.1/);
    expect(JSON.stringify(pkg.scripts)).not.toMatch(/0\.0\.0\.0|--host(?! 127)/);
  });
});
