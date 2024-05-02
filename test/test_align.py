#!/usr/bin/env python3
from pathlib import Path

import mido

import midilint

SOURCE = Path(__file__).parent / "files/bad_timing.mid"


def test_align_quarter_note():
    mid = mido.MidiFile(SOURCE, clip=True)
    mid = midilint.align(mid, 1)

    expected = [
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
    ]

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.time == expected[i]
            i += 1


def test_align_eighth():
    mid = mido.MidiFile(SOURCE, clip=True)
    mid = midilint.align(mid, 2)

    expected = [
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
    ]

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.time == expected[i]
            i += 1
