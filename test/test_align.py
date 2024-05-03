#!/usr/bin/env python3
from pathlib import Path
import pytest

import mido

import midilint

BAD_TIMING = Path(__file__).parent / "files/bad_timing.mid"
BAD_TIMING_OVERLAP = Path(__file__).parent / "files/bad_timing_overlap.mid"


@pytest.mark.parametrize(
    "source,expected",
    [
        (
            BAD_TIMING,
            [
                0,
                128,
                0,
                128,
                0,
                128,
                128,
                128,
                0,
                128,
                0,
                128,
                128,
                128,
                0,
                128,
                0,
                128,
            ],
        ),
        (
            BAD_TIMING_OVERLAP,
            [
                0,
                0,
                0,
                128,
                0,
                0,
                384,
                0,
                0,
                128,
                0,
                0,
                384,
                0,
                128,
                0,
            ],
        ),
    ],
)
def test_align_quarter_note(source, expected):
    mid = mido.MidiFile(source, clip=True)
    mid = midilint.align(mid, 1)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.time == expected[i]
            i += 1


@pytest.mark.parametrize(
    "source,expected",
    [
        (
            BAD_TIMING,
            [
                0,
                128,
                0,
                128,
                64,
                64,
                128,
                128,
                0,
                128,
                0,
                128,
                128,
                128,
                0,
                128,
                0,
                128,
            ],
        ),
        (
            BAD_TIMING_OVERLAP,
            [
                0,
                0,
                0,
                128,
                64,
                0,
                256,
                64,
                0,
                128,
                0,
                0,
                320,
                0,
                192,
                0,
            ],
        ),
    ],
)
def test_align_eighth(source, expected):
    mid = mido.MidiFile(source, clip=True)
    mid = midilint.align(mid, 2)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.time == expected[i]
            i += 1
