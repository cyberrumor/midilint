#!/usr/bin/env python3
from pathlib import Path
import pytest

import mido
import midi_abstraction as mab
import midilint


@pytest.mark.parametrize(
    "file,expected",
    [
        (
            Path(__file__).parent / "files/c4_to_c5.mid",
            {
                "type": 1,
                "ticks_per_beat": 128,
                "note_duration_min": 128,
                "note_duration_max": 128,
                "velocity_min": 64,
                "velocity_max": 64,
                "velocity_mean": 64,
                "velocity_median": 64,
                "velocity_mode": 64,
                "tonal_center": "c",
                "notes": [
                    "c",
                    "d",
                    "db",
                    "e",
                    "eb",
                    "f",
                    "g",
                    "gb",
                    "a",
                    "ab",
                    "b",
                    "bb",
                ],
                "key": "c_?",
            },
        ),
        (
            Path(__file__).parent / "files/bad_timing.mid",
            {
                "type": 1,
                "ticks_per_beat": 128,
                "note_duration_min": 8,
                "note_duration_max": 168,
                "velocity_min": 29,
                "velocity_max": 125,
                "velocity_mean": 62,
                "velocity_median": 64,
                "velocity_mode": 29,
                "tonal_center": "c",
                "notes": ["c", "d", "e"],
                "key": "c_major",
            },
        ),
        (
            Path(__file__).parent / "files/bad_timing_overlap.mid",
            {
                "type": 1,
                "ticks_per_beat": 128,
                "note_duration_min": 8,
                "note_duration_max": 304,
                "velocity_min": 29,
                "velocity_max": 124,
                "velocity_mean": 61,
                "velocity_median": 64,
                "velocity_mode": 39,
                "tonal_center": "e",
                "notes": ["e", "c", "d"],
                "key": "e_minor",
            },
        ),
    ],
)
def test_identify(file, expected):
    mid = mido.MidiFile(file, clip=True)
    result = midilint.identify(mid)
    assert result == expected
