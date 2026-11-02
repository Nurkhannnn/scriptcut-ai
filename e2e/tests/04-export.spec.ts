import { expect, test } from '@playwright/test';
import fs from 'node:fs';
import { createProjectViaApi, cutViaApi, deleteSegmentsViaApi, uniqueName } from './helpers';

test.describe('Feature: export', () => {
  test('export is disabled until a cut has completed', async ({ page, request }) => {
    const project = await createProjectViaApi(request, uniqueName('export-disabled'));
    await page.goto(`/projects/${project.id}`);
    await expect(page.getByTestId('export-button')).toBeDisabled();
    expect((await request.get(`/api/projects/${project.id}/export/download`)).status()).toBe(409);
  });

  test('downloads a valid mp4 after cutting', async ({ page, request }) => {
    const project = await createProjectViaApi(request, uniqueName('export'));
    await deleteSegmentsViaApi(request, project.id, [project.segments[0].id]);
    await cutViaApi(request, project.id);

    await page.goto(`/projects/${project.id}`);
    await expect(page.getByTestId('export-button')).toBeEnabled();

    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.getByTestId('export-button').click(),
    ]);
    expect(download.suggestedFilename()).toMatch(/\.mp4$/);

    const buf = fs.readFileSync((await download.path())!);
    expect(buf.length).toBeGreaterThan(1000);
    expect(buf.subarray(4, 8).toString('ascii')).toBe('ftyp'); // valid MP4 container
  });
});
