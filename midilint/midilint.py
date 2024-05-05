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
    note_durations = {}

    # Track all notes and velocities.
    velocities = []
    song_notes = []

    # Loop through the tracks to populate the details declared above.
    for track in source.tracks:
        for message in track:
            # A note_on can be velocity 0 which behaves like note_off.
            if message.type in ("note_on", "note_off"):
                if message.velocity != 0:
                    velocities.append(message.velocity)

                # Get a letter note from a midi pitch.
                n = set()
                for k, v in mab.NOTES.items():
                    if message.note in v:
                        n.add(k)

                if message.time < note_duration_min and message.time != 0:
                    note_duration_min = message.time
                if message.time > note_duration_max:
                    note_duration_max = message.time

                # Skip counting drum durations for tonal center
                if n is None:
                    continue

                song_notes.append(n)

                for i in n:
                    if i in note_durations:
                        note_durations[i] += message.time
                    else:
                        note_durations[i] = message.time

    identity = None
    for mode in [
        mab.MAJOR,
        mab.MINOR,
        mab.DORIAN,
        mab.PHRYGIAN,
        mab.LYDIAN,
        mab.MIXOLYDIAN,
        mab.LOCRIAN,
    ]:
        found = False
        for note in list(mab.Note):
            key = mode.notes(note)

            key_valid = True
            for n in song_notes:
                match = False
                for enharmonic_set in key:
                    if n == enharmonic_set:
                        match = True
                        break
                if not match:
                    key_valid = False
                    break

            if key_valid:
                identity = f"{note.value}_{mode.mode.value}"
                if max(note_durations.items(), key=lambda x: x[1])[0] in key[0]:
                    # If the key is the tonal center, this is probably it. This is better than
                    # listing all possible keys that have the same notes but not the same tonal
                    # center, I.e [c_minor, d_locrian, ds_ionian, f_dorian, g_phrygian, ...]
                    found = True
                    break
        if found:
            break

    if identity is None:
        # If we couldn't pin down an identity, we're working with a key with borrowed
        # chords. Instead of trying to guess the closest key, just ID it by the tonal
        # center + question mark.
        identity = f"{max(note_durations.items(), key=lambda x: x[1])[0].value}_?"

    # Get the canonical order for the notes
    notes = set()
    for s in song_notes:
        notes |= s
    notes = sorted(list(notes))
    start = notes.index(identity.split("_")[0])
    notes = [i.value for i in notes[start:] + notes[:start]]

    # Remove the undesired variant of enharmonic equivalent notes.
    for n in notes:
        # When given a choice of enharmonic pairs, keep the variant
        # that does not already have a single letter earlier in the scale.
        # E.g. ['c', 'd', 'ds', 'eb'], remove 'ds'.
        if (pair := mab.ENHARMONIC.get(n, None)) is not None:
            if pair in notes and pair[0] in [i[0] for i in notes]:
                notes.remove(n)

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
        "tonal_center": max(note_durations.items(), key=lambda x: x[1])[0].value,
        "notes": notes,
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


def snap(
    source: mido.MidiFile,
    key: list[set[mab.Note]],
) -> mido.MidiFile:
    """
    Snap pitches to their nearest note in the key.
    """
    notes = []
    for enharmonic_set in key:
        notes.extend(mab.NOTES[next(iter(enharmonic_set))])

    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                message.note = min(notes, key=lambda x: abs(x - message.note))
    return source


def transpose(
    source: mido.MidiFile,
    key: list[set[mab.Note]],
) -> mido.MidiFile:
    """
    Transpose based on scale degrees. Requires an identifiable key.
    """
    original_key = identify(source)["key"]
    if "?" in original_key:
        raise ValueError("original key is unidentifiable, unable to transpose.")

    note, mode = original_key.split("_")
    original_key = getattr(mab, mode.upper()).notes(note)

    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                note = None
                for k, v in mab.NOTES.items():
                    if message.note in v:
                        note = k
                        break

                if note is None:
                    # Note sure why this would happen, but still.
                    continue

                for degree, s in enumerate(original_key):
                    if note in s:
                        break

                new = mab.NOTES[mab.Note(next(iter(key[degree])))]

                # Get the note that's closest to the original octave.
                message.note = min(new, key=lambda x: abs(x - message.note))

    return source
