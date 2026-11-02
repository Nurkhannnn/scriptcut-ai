import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

export default async function globalSetup() {
  const dir = path.resolve(__dirname, 'fixtures');
  const out = path.join(dir, 'sample.mp4');
  if (existsSync(out)) return;
  mkdirSync(dir, { recursive: true });
  // 10 s, 320x240 test video with audio (stub transcriber yields 5 x 2 s segments). Requires ffmpeg on the host.
  execFileSync('ffmpeg', [
    '-y', '-f', 'lavfi', '-i', 'testsrc=duration=10:size=320x240:rate=15',
    '-f', 'lavfi', '-i', 'sine=frequency=440:duration=10',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out,
  ]);
}
