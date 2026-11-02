---
name: "[E2E] Video cut execution"
about: Track the Playwright E2E suite for executing cuts
title: "[E2E] Video cut execution"
labels: e2e-test
---

## Feature
Deleted transcript segments are cut from the video with ffmpeg.

## Spec
`e2e/tests/03-video-cut.spec.ts` · run: `npm --prefix e2e run test:cut`

## Preconditions
- Stack running: `docker compose up -d --build --wait` (`TRANSCRIBE_PROVIDER=stub`)
- `ffmpeg` on the host (fixture `e2e/fixtures/sample.mp4` is auto-generated)

## Test cases
- [ ] Delete segments 2 and 4, cut, status done, duration about 6 s
- [ ] All segments deleted: cut button disabled, API returns 409
- [ ] Re-cut after more edits yields the new shorter duration

## Acceptance criteria
- [ ] All cases pass on CI (chromium)
- [ ] No flaky retries over 10 consecutive runs
