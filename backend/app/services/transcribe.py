from pathlib import Path

from app.config import get_settings


def transcribe(video: Path, duration: float) -> list[dict]:
    """Return [{start, end, text}, ...]. 'stub' is deterministic (used in CI/E2E).

    Wire a real provider (Whisper, etc.) by adding a branch below.
    """
    provider = get_settings().transcribe_provider
    if provider == "stub":
        step, segs, t, i = 2.0, [], 0.0, 1
        while t < duration - 0.01:
            end = min(t + step, duration)
            segs.append({"start": round(t, 3), "end": round(end, 3), "text": f"Segment {i}: placeholder transcript."})
            t, i = end, i + 1
        return segs
    raise NotImplementedError(f"Transcription provider '{provider}' is not configured")
