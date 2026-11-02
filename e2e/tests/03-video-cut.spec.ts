import { expect, test } from '@playwright/test';
import { createProjectViaApi, deleteSegmentsViaApi, uniqueName } from './helpers';

test.describe('Feature: video cut execution', () => {
  test('cuts deleted segments and produces a shorter video', async ({ page, request }) => {
    const project = await createProjectViaApi(request, uniqueName('cut'));
    await page.goto(`/projects/${project.id}`);

    await page.getByTestId('transcript-segment').nth(1).getByTestId('segment-delete-toggle').click();
    await page.getByTestId('transcript-segment').nth(3).getByTestId('segment-delete-toggle').click();
    await expect(page.getByTestId('save-status')).toHaveText(/saved/i);

    await page.getByTestId('cut-button').click();
    await expect(page.getByTestId('cut-status')).toHaveText(/done/i, { timeout: 60_000 });

    const exp = await (await request.get(`/api/projects/${project.id}/export`)).json();
    expect(exp.status).toBe('done');
    expect(exp.duration).toBeGreaterThan(5.4); // ~10 s - 2 x 2 s = 6 s
    expect(exp.duration).toBeLessThan(6.6);
  });

  test('cut is unavailable when every segment is deleted', async ({ page, request }) => {
    const project = await createProjectViaApi(request, uniqueName('cut-empty'));
    await deleteSegmentsViaApi(request, project.id, project.segments.map((s) => s.id));
    await page.goto(`/projects/${project.id}`);
    await expect(page.getByTestId('cut-button')).toBeDisabled();
    expect((await request.post(`/api/projects/${project.id}/cut`)).status()).toBe(409);
  });

  test('re-cutting after further edits reflects the new duration', async ({ page, request }) => {
    const project = await createProjectViaApi(request, uniqueName('recut'));
    await page.goto(`/projects/${project.id}`);

    await page.getByTestId('transcript-segment').first().getByTestId('segment-delete-toggle').click();
    await expect(page.getByTestId('save-status')).toHaveText(/saved/i);
    await page.getByTestId('cut-button').click();
    await expect(page.getByTestId('cut-status')).toHaveText(/done/i, { timeout: 60_000 });

    await page.getByTestId('transcript-segment').nth(1).getByTestId('segment-delete-toggle').click();
    await expect(page.getByTestId('save-status')).toHaveText(/saved/i);
    await page.getByTestId('cut-button').click();
    await expect
      .poll(async () => (await (await request.get(`/api/projects/${project.id}/export`)).json()).duration, {
        timeout: 60_000,
      })
      .toBeLessThan(6.6);
  });
});
