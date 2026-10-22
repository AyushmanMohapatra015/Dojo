import '@testing-library/jest-dom/vitest';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// jsdom has no ResizeObserver, which Recharts' ResponsiveContainer needs.
class StubResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
if (!globalThis.ResizeObserver) globalThis.ResizeObserver = StubResizeObserver;

afterEach(() => {
  cleanup();
});
