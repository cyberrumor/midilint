#!/usr/bin/env python3
from pathlib import Path
import pytest

import mido
import midi_abstraction as mab
import midilint

SOURCE = Path(__file__).parent / "files/c4_to_c5.mid"


@pytest.mark.parametrize(
    "key,expected",
    [
        (
            "c_major",
            [
                60,
                60,
                60,
                60,
                62,
                62,
                62,
                62,
                64,
                64,
                65,
                65,
                65,
                65,
                67,
                67,
                67,
                67,
                69,
                69,
                69,
                69,
                71,
                71,
                72,
                72,
            ],
        ),
        (
            "c_minor",
            [
                60,
                60,
                60,
                60,
                62,
                62,
                63,
                63,
                63,
                63,
                65,
                65,
                65,
                65,
                67,
                67,
                68,
                68,
                68,
                68,
                70,
                70,
                72,
                72,
                72,
                72,
            ],
        ),
        (
            "g_mixolydian",
            [
                60,
                60,
                60,
                60,
                62,
                62,
                62,
                62,
                64,
                64,
                65,
                65,
                67,
                67,
                67,
                67,
                67,
                67,
                69,
                69,
                69,
                69,
                71,
                71,
                72,
                72,
            ],
        ),
    ],
)
def test_snap(key, expected):
    mid = mido.MidiFile(SOURCE, clip=True)
    note, mode = key.split("_")
    notes = getattr(mab, mode.upper()).notes(note)
    mid = midilint.snap(mid, notes)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.note == expected[i]
            i += 1
