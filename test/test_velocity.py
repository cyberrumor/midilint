#!/usr/bin/env python3
from pathlib import Path

import mido

import midilint

SOURCE = Path(__file__).parent / "files/bad_timing.mid"


def test_normalize():
    velocity = 100
    mid = mido.MidiFile(SOURCE, clip=True)
    mid = midilint.normalize(mid, velocity)
    for track in mid.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                assert message.velocity == velocity
