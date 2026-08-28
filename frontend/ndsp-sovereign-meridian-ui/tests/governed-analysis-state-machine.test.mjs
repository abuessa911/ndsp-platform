import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import test from 'node:test';

const root = process.cwd();
const out = mkdtempSync(join(tmpdir(), 'ndsp-state-machine-'));

process.on('exit', () => rmSync(out, { recursive: true, force: true }));

execFileSync(
  process.platform === 'win32' ? 'npx.cmd' : 'npx',
  [
    'tsc',
    '--ignoreConfig',
    'src/analysis/stateMachine.ts',
    '--target', 'ES2022',
    '--module', 'ESNext',
    '--moduleResolution', 'Bundler',
    '--outDir', out,
    '--skipLibCheck',
  ],
  { cwd: root, stdio: 'inherit' },
);

writeFileSync(join(out, 'package.json'), JSON.stringify({ type: 'module' }));

const {
  buildNextGovernedContext,
  deriveResultLifecycleState,
  sameCalculationContext,
} = await import(pathToFileURL(join(out, 'stateMachine.js')).href);

const baseSelection = Object.freeze({
  market: 'crypto',
  symbol: 'BTCUSDT',
  timeframe: 'weekly',
  analysisMode: 'speculative',
  presentationMode: 'beginner',
});

function context(overrides = {}) {
  return {
    ...baseSelection,
    asOf: '2026-08-28T15:00:00Z',
    generation: 7,
    ...overrides,
  };
}

test('first validated context starts generation 1', () => {
  const next = buildNextGovernedContext(null, baseSelection, '2026-08-28T16:00:00Z');
  assert.equal(next.generation, 1);
});

test('presentation-only change does not invalidate calculation generation', () => {
  const previous = context();
  const selection = { ...baseSelection, presentationMode: 'professional' };
  assert.equal(sameCalculationContext(previous, selection), true);
  const next = buildNextGovernedContext(previous, selection, '2026-08-28T16:00:00Z');
  assert.equal(next.generation, 7);
  assert.equal(next.presentationMode, 'professional');
});

for (const [field, value] of [
  ['market', 'forex'],
  ['symbol', 'ETHUSDT'],
  ['timeframe', 'daily'],
  ['analysisMode', 'investment'],
]) {
  test(`${field} change invalidates prior calculation generation`, () => {
    const previous = context();
    const selection = { ...baseSelection, [field]: value };
    assert.equal(sameCalculationContext(previous, selection), false);
    const next = buildNextGovernedContext(previous, selection, '2026-08-28T16:00:00Z');
    assert.equal(next.generation, 8);
  });
}

test('result lifecycle is deterministic and fail-closed', () => {
  const common = {
    loading: false,
    hasError: false,
    hasCoverage: true,
    globalRegistryReconciled: true,
    decisionReady: false,
    officialState: null,
    capabilityStates: [],
  };

  assert.equal(deriveResultLifecycleState({ ...common, loading: true }), 'loading');
  assert.equal(deriveResultLifecycleState({ ...common, hasError: true }), 'unavailable');
  assert.equal(deriveResultLifecycleState({ ...common, hasCoverage: false }), 'unavailable');
  assert.equal(deriveResultLifecycleState({ ...common, capabilityStates: ['STALE'] }), 'stale');
  assert.equal(deriveResultLifecycleState({ ...common, globalRegistryReconciled: false }), 'blocked');
  assert.equal(deriveResultLifecycleState({ ...common, decisionReady: true, officialState: 'READY' }), 'ready');
  assert.equal(deriveResultLifecycleState({ ...common, officialState: 'BLOCKED' }), 'blocked');
  assert.equal(deriveResultLifecycleState({ ...common, capabilityStates: ['BLOCKED'] }), 'blocked');
  assert.equal(deriveResultLifecycleState({ ...common, capabilityStates: ['PARTIAL'] }), 'partial');
  assert.equal(deriveResultLifecycleState({ ...common, capabilityStates: ['UNAVAILABLE'] }), 'partial');
  assert.equal(deriveResultLifecycleState(common), 'blocked');
});

test('contradictory READY evidence never overrides blocking evidence', () => {
  const readyBase = {
    loading: false,
    hasError: false,
    hasCoverage: true,
    globalRegistryReconciled: true,
    decisionReady: true,
    officialState: 'READY',
    capabilityStates: [],
  };

  assert.equal(
    deriveResultLifecycleState({ ...readyBase, capabilityStates: ['BLOCKED'] }),
    'blocked',
  );
  assert.equal(
    deriveResultLifecycleState({ ...readyBase, officialState: 'BLOCKED' }),
    'blocked',
  );
  assert.equal(
    deriveResultLifecycleState({ ...readyBase, capabilityStates: ['STALE'] }),
    'stale',
  );
});
