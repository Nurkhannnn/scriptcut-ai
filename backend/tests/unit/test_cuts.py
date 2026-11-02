from dataclasses import dataclass

from app.services.cuts import keep_ranges


@dataclass
class S:
    start: float
    end: float
    deleted: bool = False


def test_all_kept_merges_adjacent():
    assert keep_ranges([S(0, 2), S(2, 4), S(4, 6)]) == [(0, 6)]


def test_deleted_middle_splits_ranges():
    assert keep_ranges([S(0, 2), S(2, 4, True), S(4, 6)]) == [(0, 2), (4, 6)]


def test_all_deleted_is_empty():
    assert keep_ranges([S(0, 2, True), S(2, 4, True)]) == []


def test_unsorted_input_and_zero_length_ignored():
    assert keep_ranges([S(4, 6), S(1, 1), S(0, 2)]) == [(0, 2), (4, 6)]
