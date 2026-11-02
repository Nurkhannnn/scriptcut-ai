---
name: "[E2E] Export"
about: Track the Playwright E2E suite for exporting the final video
title: "[E2E] Export"
labels: e2e-test
---

## Feature
User downloads the cut video as an MP4.

## Spec
`e2e/tests/04-export.spec.ts` · run: `npm --prefix e2e run test:export`

## Preconditions
- Stack running: `docker compose up -d --build --wait` (`TRANSCRIBE_PROVIDER=stub`)
- `ffmpeg` on the host (fixture `e2e/fixtures/sample.mp4` is auto-generated)

## Test cases
- [ ] Export disabled and API returns 409 before any cut
- [ ] After a cut, export downloads a valid .mp4

## Acceptance criteria
- [ ] All cases pass on CI (chromium)
- [ ] No flaky retries over 10 consecutive runs
