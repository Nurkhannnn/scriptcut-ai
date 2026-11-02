---
name: "[E2E] Project creation"
about: Track the Playwright E2E suite for project creation
title: "[E2E] Project creation"
labels: e2e-test
---

## Feature
User names a project and uploads a video; a transcript is generated.

## Spec
`e2e/tests/01-project-creation.spec.ts` · run: `npm --prefix e2e run test:project`

## Preconditions
- Stack running: `docker compose up -d --build --wait` (`TRANSCRIBE_PROVIDER=stub`)
- `ffmpeg` on the host (fixture `e2e/fixtures/sample.mp4` is auto-generated)

## Test cases
- [ ] Create project: redirect to editor, player + 5 transcript + 5 timeline segments
- [ ] Project is listed on dashboard and persists after reload
- [ ] Submit without video shows form error, no navigation
- [ ] Non-video upload is rejected and error is shown

## Acceptance criteria
- [ ] All cases pass on CI (chromium)
- [ ] No flaky retries over 10 consecutive runs
