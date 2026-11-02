import { APIRequestContext, Page, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

export const SAMPLE_VIDEO = path.resolve(__dirname, '../fixtures/sample.mp4');

export const uniqueName = (prefix: string) =>
  `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

export async function createProjectViaUi(page: Page, name: string): Promise<string> {
  await page.goto('/');
  await page.getByTestId('new-project-button').click();
  await page.getByTestId('project-name-input').fill(name);
  await page.getByTestId('video-file-input').setInputFiles(SAMPLE_VIDEO);
  await page.getByTestId('create-project-submit').click();
  await page.waitForURL(/\/projects\/[0-9a-f-]{36}$/);
  return page.url().split('/').pop()!;
}

export async function createProjectViaApi(request: APIRequestContext, name: string) {
  const res = await request.post('/api/projects', {
    multipart: {
      name,
      video: { name: 'sample.mp4', mimeType: 'video/mp4', buffer: fs.readFileSync(SAMPLE_VIDEO) },
    },
  });
  expect(res.status()).toBe(201);
  return res.json() as Promise<{ id: string; duration: number; segments: { id: number }[] }>;
}

export async function deleteSegmentsViaApi(request: APIRequestContext, projectId: string, ids: number[]) {
  for (const id of ids) {
    const res = await request.patch(`/api/projects/${projectId}/segments/${id}`, { data: { deleted: true } });
    expect(res.ok()).toBeTruthy();
  }
}

export async function cutViaApi(request: APIRequestContext, projectId: string) {
  expect((await request.post(`/api/projects/${projectId}/cut`)).status()).toBe(202);
  await expect
    .poll(async () => (await (await request.get(`/api/projects/${projectId}/export`)).json()).status, { timeout: 60_000 })
    .toBe('done');
  return (await request.get(`/api/projects/${projectId}/export`)).json() as Promise<{ duration: number }>;
}
