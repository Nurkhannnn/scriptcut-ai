import { describe, expect, it } from 'vitest';
import { fmt } from './utils';

describe('fmt', () => {
  it('formats seconds as m:ss', () => {
    expect(fmt(0)).toBe('0:00');
    expect(fmt(65.9)).toBe('1:05');
  });
  it('clamps negatives', () => {
    expect(fmt(-3)).toBe('0:00');
  });
});
