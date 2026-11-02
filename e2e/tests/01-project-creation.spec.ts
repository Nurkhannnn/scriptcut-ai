import { expect, test } from '@playwright/test';
import { createProjectViaUi, uniqueName } from './helpers';

test.describe('Feature: project creation', () => {
  test('creates a project from an uploaded video and renders the transcript', async ({ page }) => {
    await createProjectViaUi(page, uniqueName('create'));
    await expect(page.getByTestId('video-player')).toBeVisible();
    await expect(page.getByTestId('transcript-segment')).toHaveCount(5);
    await expect(page.getByTestId('timeline-segment')).toHaveCount(5);
  });

  test('new project appears on the dashboard and survives reload', async ({ page }) => {
    const name = uniqueName('list');
    await createProjectViaUi(page, name);
    await page.goto('/');
    await expect(page.getByTestId('project-list-item').filter({ hasText: name })).toBeVisible();
    await page.reload();
    await expect(page.getByTestId('project-list-item').filter({ hasText: name })).toBeVisible();
  });

  test('blocks submission when no video is selected', async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('new-project-button').click();
    await page.getByTestId('project-name-input').fill(uniqueName('novideo'));
    await page.getByTestId('create-project-submit').click();
    await expect(page.getByTestId('form-error')).toBeVisible();
    await expect(page).not.toHaveURL(/\/projects\//);
  });

  test('rejects a non-video upload', async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('new-project-button').click();
    await page.getByTestId('project-name-input').fill(uniqueName('badfile'));
    await page.getByTestId('video-file-input').setInputFiles({
      name: 'notes.txt', mimeType: 'text/plain', buffer: Buffer.from('not a video'),
    });
    await page.getByTestId('create-project-submit').click();
    await expect(page.getByTestId('form-error')).toBeVisible();
  });
});
