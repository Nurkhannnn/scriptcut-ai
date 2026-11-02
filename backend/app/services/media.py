import subprocess
from pathlib import Path

from app.config import get_settings


class MediaError(RuntimeError):
    pass


def project_dir(project_id: str) -> Path:
    path = Path(get_settings().media_dir) / project_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def probe_duration(path: Path) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True, timeout=60,
        ).stdout.strip()
        return float(out)
    except (subprocess.SubprocessError, ValueError) as exc:
        raise MediaError("Unable to read video duration; is this a valid video file?") from exc


def render_cut(src: Path, ranges: list[tuple[float, float]], out: Path) -> None:
    """Trim + concat kept ranges into one H.264/AAC mp4 (assumes an audio track)."""
    if not ranges:
        raise MediaError("Nothing left to export")
    parts, labels = [], []
    for i, (s, e) in enumerate(ranges):
        parts.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(ranges)}:v=1:a=1[v][a]"
    cmd = ["ffmpeg", "-y", "-i", str(src), "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-movflags", "+faststart", str(out)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if proc.returncode != 0:
        raise MediaError(f"ffmpeg failed: {proc.stderr[-300:]}")
