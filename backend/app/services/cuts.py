"""Pure cut logic: easy to unit-test, no I/O."""
from collections.abc import Iterable
from typing import Protocol


class SegmentLike(Protocol):
    start: float
    end: float
    deleted: bool


def keep_ranges(segments: Iterable[SegmentLike], merge_gap: float = 0.05) -> list[tuple[float, float]]:
    """Return merged (start, end) ranges of non-deleted segments, in time order."""
    ranges: list[tuple[float, float]] = []
    for seg in sorted(segments, key=lambda s: s.start):
        if seg.deleted or seg.end <= seg.start:
            continue
        if ranges and seg.start - ranges[-1][1] <= merge_gap:
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], seg.end))
        else:
            ranges.append((seg.start, seg.end))
    return ranges
