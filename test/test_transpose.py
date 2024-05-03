#!/usr/bin/env python3
from pathlib import Path
import pytest

import mido
import midi_abstraction
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
                70,
                70,
                72,
                72,
            ],
        ),
        (
            "e_phrygian",
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
    ],
)
def test_correct_pitch_shift_down(key, expected):
    mid = mido.MidiFile(SOURCE, clip=True)
    key = midi_abstraction.Key(key)
    mid = midilint.correct_pitch(mid, key, midilint.shift_down)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.note == expected[i]
            i += 1


@pytest.mark.parametrize(
    "key,expected",
    [
        (
            "c_major",
            [
                60,
                60,
                62,
                62,
                62,
                62,
                64,
                64,
                64,
                64,
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
                62,
                62,
                62,
                62,
                63,
                63,
                65,
                65,
                65,
                65,
                67,
                67,
                67,
                67,
                68,
                68,
                70,
                70,
                70,
                70,
                72,
                72,
                72,
                72,
            ],
        ),
        (
            "e_dorian",
            [
                61,
                61,
                61,
                61,
                62,
                62,
                64,
                64,
                64,
                64,
                66,
                66,
                66,
                66,
                67,
                67,
                69,
                69,
                69,
                69,
                71,
                71,
                71,
                71,
                73,
                73,
            ],
        ),
    ],
)
def test_correct_pitch_shift_up(key, expected):
    mid = mido.MidiFile(SOURCE, clip=True)
    key = midi_abstraction.Key(key)
    mid = midilint.correct_pitch(mid, key, midilint.shift_up)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.note == expected[i]
            i += 1


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
def test_correct_pitch_shift_nearest(key, expected):
    mid = mido.MidiFile(SOURCE, clip=True)
    key = midi_abstraction.Key(key)
    mid = midilint.correct_pitch(mid, key, midilint.shift_nearest)

    i = 0
    for track in mid.tracks:
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue
            assert message.note == expected[i]
            i += 1
