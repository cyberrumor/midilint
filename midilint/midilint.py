#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from typing import Callable

import mido
import midi_abstraction as mab


def identify(source: mido.MidiFile) -> mido.MidiFile:
    """
    Get information about a file.
    """
    # Note durations
    note_duration_min = 2**31 - 1
    note_duration_max = 0
    velocities = []

    song_notes = {}

    for track in source.tracks:
        for message in track:
            # A note_on can be velocity 0 which behaves like note_off.
            if message.type in ("note_on", "note_off"):
                if message.velocity != 0:
                    velocities.append(message.velocity)


                # Get a letter note from a midi pitch.
                n = None
                for k, v in mab.NOTES.items():
                    if message.note in v:
                        n = k
                        break

                if message.time < note_duration_min and message.time != 0:
                    note_duration_min = message.time
                if message.time > note_duration_max:
                    note_duration_max = message.time

                # Skip counting drum durations for tonal center
                if n is None:
                    continue

                if n in song_notes:
                    song_notes[n] += message.time
                else:
                    song_notes[n] = message.time

    identity = "unknown"
    possible_keys = []
    for mode in list(mab.Mode):
        for note in list(mab.Note):
            key = getattr(mab, mode.name).notes(note)

            key_valid = True
            for n in song_notes:
                match = False
                for enharmonic_set in key:
                    if n in enharmonic_set:
                        match = True
                        break
                if not match:
                    key_valid = False
                    break

            if key_valid and max(notes.items(), key=lambda x: x[1])[0] in key[0]:
                # If the key is the tonal center, this is probably it.
                identity = f"{note.value}_{mode.value}"

    results = {
        "type": source.type,
        "ticks_per_beat": source.ticks_per_beat,
        "note_duration_min": note_duration_min,
        "note_duration_max": note_duration_max,
        "velocity_min": min(velocities),
        "velocity_max": max(velocities),
        "velocity_mean": sum(velocities) // len(velocities),
        "velocity_median": sorted(velocities)[len(velocities) // 2],
        "velocity_mode": max(velocities, key=lambda x: velocities.count(x)),
        "tonal_center": max(notes.items(), key=lambda x: x[1])[0],
        "notes": " ".join([i[0] for i in sorted(song_notes.items(), key=lambda x: x[1], reverse=True)]),
        "key": identity,
    }
    return results


def normalize(source: mido.MidiFile, velocity: int) -> mido.MidiFile:
    """
    Normalize messages in source to input velocity and return source.
    """
    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                message.velocity = velocity
    return source


def align(source: mido.MidiFile, precision: int = 1) -> mido.MidiFile:
    """
    Align the start and ends of notes to the quarter note intervals, aka the beat.

    Since the duration of notes are relative (at least when source.type == 1),
    shifting a note changes the absolute position of all the notes after it.
    To prevent shortening or lengthening, we have to track how far the previous
    note was shifted and accommodate the note after it.
    """
    if source.ticks_per_beat % 2 != 0:
        raise ValueError(
            f"Found track with {source.ticks_per_beat=} which was required to divisible by 2."
        )

    if precision > 1 and precision % 2 != 0:
        raise ValueError(
            f"Found argument {precision=} which was required to be 1 or divisible by 2."
        )

    tick = source.ticks_per_beat // precision

    for track in source.tracks:
        shift = 0
        for message in track:
            if message.type not in ("note_on", "note_off"):
                continue

            if message.time + shift % tick != 0:
                original = message.time + shift
                message.time = tick * round((message.time + shift) / tick)
                shift = original - message.time

    return source


def correct_pitch(
    source: mido.MidiFile,
    key: list[set[mab.Note]],
) -> mido.MidiFile:
    """
    Snap pitches to notes in the given key via the strategy.
    """
    notes = []
    for enharmonic_set in key:
        notes.extend(mab.NOTES[next(iter(enharmonic_set))])

    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                message.note = min(notes, key=lambda x: abs(x - message.note))
    return source
