import { expect, test } from '@playwright/test';
import { createProjectViaApi, uniqueName } from './helpers';

test.describe('Feature: text editing and timeline sync', () => {
  let projectId: string;

  test.beforeEach(async ({ page, request }) => {
    projectId = (await createProjectViaApi(request, uniqueName('sync'))).id;
    await page.goto(`/projects/${projectId}`);
    await expect(page.getByTestId('transcript-segment')).toHaveCount(5);
  });

  test('edited transcript text is saved and persists after reload', async ({ page }) => {
    const input = page.getByTestId('transcript-segment').first().getByTestId('segment-text');
    await input.fill('Edited by Playwright');
    await input.blur();
    await expect(page.getByTestId('save-status')).toHaveText(/saved/i);
    await page.reload();
    await expect(page.getByTestId('transcript-segment').first().getByTestId('segment-text')).toHaveValue(
      'Edited by Playwright',
    );
  });

  test('deleting a transcript segment marks it on the timeline, restoring reverts both', async ({ page }) => {
    const seg = page.getByTestId('transcript-segment').nth(1);
    const tl = page.getByTestId('timeline-segment').nth(1);

    await seg.getByTestId('segment-delete-toggle').click();
    await expect(seg).toHaveAttribute('data-deleted', 'true');
    await expect(tl).toHaveAttribute('data-deleted', 'true');

    await seg.getByTestId('segment-delete-toggle').click();
    await expect(seg).toHaveAttribute('data-deleted', 'false');
    await expect(tl).toHaveAttribute('data-deleted', 'false');
  });

  test('deletions persist on the server across reload', async ({ page, request }) => {
    await page.getByTestId('transcript-segment').nth(2).getByTestId('segment-delete-toggle').click();
    await expect(page.getByTestId('save-status')).toHaveText(/saved/i);
    await page.reload();
    await expect(page.getByTestId('transcript-segment').nth(2)).toHaveAttribute('data-deleted', 'true');
    const project = await (await request.get(`/api/projects/${projectId}`)).json();
    expect(project.segments[2].deleted).toBe(true);
  });

  test('clicking play on a segment seeks the video to its start time', async ({ page }) => {
    const seg = page.getByTestId('transcript-segment').nth(3);
    const start = Number(await seg.getAttribute('data-start'));
    await seg.getByTestId('segment-play').click();
    await expect
      .poll(() => page.getByTestId('video-player').evaluate((v: HTMLVideoElement) => v.currentTime), { timeout: 10_000 })
      .toBeGreaterThanOrEqual(start - 0.5);
  });
});
