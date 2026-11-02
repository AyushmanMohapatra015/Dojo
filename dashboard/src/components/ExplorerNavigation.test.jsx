/**
 * ExplorerNavigation.test.jsx
 *
 * Vitest + React Testing Library + user-event
 * Import path targets the intended installed location, not the .proposed.txt filename.
 *
 * STATUS: UNEXECUTED — see integration-note.md
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ExplorerNavigation from './ExplorerNavigation.jsx';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function setup(activeView = 'overview', onViewChange = vi.fn()) {
  const utils = render(
    <ExplorerNavigation
      activeView={activeView}
      onViewChange={onViewChange}
      contentId="explorer-content"
    />,
  );
  const nav = screen.getByRole('navigation', { name: 'Results views' });
  return { ...utils, nav, onViewChange };
}

const ALL_LABELS = ['Overview', 'Compare', 'Runs', 'Method'];

// ---------------------------------------------------------------------------
// 1. All four labeled native buttons are exposed inside the named navigation.
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — structure', () => {
  it('renders four buttons with correct labels inside the named nav', () => {
    const { nav } = setup('overview');
    const buttons = within(nav).getAllByRole('button');
    expect(buttons).toHaveLength(4);
    ALL_LABELS.forEach((label) => {
      expect(within(nav).getByRole('button', { name: label })).toBeInTheDocument();
    });
  });
});

// ---------------------------------------------------------------------------
// 2. Only the active button has aria-current="page"; every button targets contentId.
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — aria attributes', () => {
  it('marks only the active button with aria-current="page"', () => {
    const { nav } = setup('compare');
    const current = within(nav).getByRole('button', { name: 'Compare' });
    expect(current).toHaveAttribute('aria-current', 'page');

    ['Overview', 'Runs', 'Method'].forEach((label) => {
      expect(within(nav).getByRole('button', { name: label })).not.toHaveAttribute(
        'aria-current',
      );
    });
  });

  it('every button has aria-controls pointing to the supplied contentId', () => {
    render(<ExplorerNavigation activeView="runs" onViewChange={vi.fn()} contentId="custom-results" />);
    const nav = screen.getByRole('navigation', { name: 'Results views' });
    const buttons = within(nav).getAllByRole('button');
    buttons.forEach((btn) => {
      expect(btn).toHaveAttribute('aria-controls', 'custom-results');
    });
  });

  it('uses the default contentId "explorer-content" when none is supplied', () => {
    render(
      <ExplorerNavigation activeView="overview" onViewChange={vi.fn()} />,
    );
    const buttons = screen.getAllByRole('button');
    buttons.forEach((btn) => {
      expect(btn).toHaveAttribute('aria-controls', 'explorer-content');
    });
  });
});

// ---------------------------------------------------------------------------
// 3. Clicking a different view emits its ID exactly once; current does not change
//    internally (the parent owns state — re-render is not triggered here).
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — click another view', () => {
  it('calls onViewChange once with the clicked view ID', async () => {
    const user = userEvent.setup();
    const { nav, onViewChange } = setup('overview');

    await user.click(within(nav).getByRole('button', { name: 'Runs' }));

    expect(onViewChange).toHaveBeenCalledTimes(1);
    expect(onViewChange).toHaveBeenCalledWith('runs');
  });

  it('does not internally change the current indicator after click (parent owns state)', async () => {
    const user = userEvent.setup();
    const { nav, onViewChange } = setup('overview');

    await user.click(within(nav).getByRole('button', { name: 'Compare' }));

    // aria-current stays on Overview because we did not re-render with a new prop
    expect(within(nav).getByRole('button', { name: 'Overview' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    expect(within(nav).getByRole('button', { name: 'Compare' })).not.toHaveAttribute(
      'aria-current',
    );
    expect(onViewChange).toHaveBeenCalledWith('compare');
  });
});

// ---------------------------------------------------------------------------
// 4. Re-rendering with a new activeView prop updates the current indicator.
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — re-render updates current indicator', () => {
  it('moves aria-current to the newly active view on re-render', () => {
    const onViewChange = vi.fn();
    const { rerender } = render(
      <ExplorerNavigation
        activeView="overview"
        onViewChange={onViewChange}
        contentId="explorer-content"
      />,
    );

    expect(screen.getByRole('button', { name: 'Overview' })).toHaveAttribute(
      'aria-current',
      'page',
    );

    rerender(
      <ExplorerNavigation
        activeView="method"
        onViewChange={onViewChange}
        contentId="explorer-content"
      />,
    );

    expect(screen.getByRole('button', { name: 'Method' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    expect(screen.getByRole('button', { name: 'Overview' })).not.toHaveAttribute(
      'aria-current',
    );
  });
});

// ---------------------------------------------------------------------------
// 5. Clicking the active view does not call onViewChange.
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — click active view', () => {
  it('does not call onViewChange when the active button is clicked', async () => {
    const user = userEvent.setup();
    const { nav, onViewChange } = setup('runs');

    await user.click(within(nav).getByRole('button', { name: 'Runs' }));

    expect(onViewChange).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// 6. Tab focus followed by Enter/Space can select a different view.
// ---------------------------------------------------------------------------
describe('ExplorerNavigation — keyboard activation', () => {
  it('activates a view with Enter key when focused', async () => {
    const user = userEvent.setup();
    const onViewChange = vi.fn();
    render(
      <ExplorerNavigation
        activeView="overview"
        onViewChange={onViewChange}
        contentId="explorer-content"
      />,
    );

    // Tab to the Compare button (second in DOM order)
    await user.tab();
    await user.tab();
    const compareBtn = screen.getByRole('button', { name: 'Compare' });
    expect(compareBtn).toHaveFocus();

    await user.keyboard('{Enter}');
    expect(onViewChange).toHaveBeenCalledTimes(1);
    expect(onViewChange).toHaveBeenCalledWith('compare');
  });

  it('activates a view with Space key when focused', async () => {
    const user = userEvent.setup();
    const onViewChange = vi.fn();
    render(
      <ExplorerNavigation
        activeView="overview"
        onViewChange={onViewChange}
        contentId="explorer-content"
      />,
    );

    await user.tab();
    await user.tab();
    await user.tab();
    const runsBtn = screen.getByRole('button', { name: 'Runs' });
    expect(runsBtn).toHaveFocus();

    await user.keyboard(' ');
    expect(onViewChange).toHaveBeenCalledTimes(1);
    expect(onViewChange).toHaveBeenCalledWith('runs');
  });
});
