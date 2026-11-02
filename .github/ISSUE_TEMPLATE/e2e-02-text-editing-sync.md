---
name: "[E2E] Text editing sync"
about: Track the Playwright E2E suite for transcript/timeline sync
title: "[E2E] Text editing sync"
labels: e2e-test
---

## Feature
Editing or deleting transcript text updates the timeline and is persisted.

## Spec
`e2e/tests/02-text-editing-sync.spec.ts` · run: `npm --prefix e2e run test:sync`

## Preconditions
- Stack running: `docker compose up -d --build --wait` (`TRANSCRIBE_PROVIDER=stub`)
- `ffmpeg` on the host (fixture `e2e/fixtures/sample.mp4` is auto-generated)

## Test cases
- [ ] Edited text shows Saved and persists after reload
- [ ] Deleting a segment marks transcript AND timeline; restoring reverts both
- [ ] Deletions persist server-side
- [ ] Play button seeks the video to the segment start

## Acceptance criteria
- [ ] All cases pass on CI (chromium)
- [ ] No flaky retries over 10 consecutive runs
