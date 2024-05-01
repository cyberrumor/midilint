#!/usr/bin/env python3

import mido
import sys
import argparse
import bisect
from itertools import product
from pathlib import Path
from typing import Callable

import midi_abstraction

def normalize(source: mido.MidiFile, velocity: int) -> mido.MidiFile:
    """
    Normalize messages in source to input velocity and return source.
    """
    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                message.velocity = velocity
    return source


def shift_up(track: mido.MidiTrack, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes up.
    """
    for message in track:
        if message.type in ("note_on", "note_off"):
            # Raise the note until it's in the key.
            while message.note < 127 and message.note not in notes:
                message.note += 1
            # If we raised it too high, we will have to do the opposite.
            while message.note > 0 and message.note not in notes:
                message.note -= 1


def shift_down(track: mido.MidiTrack, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes down.
    """
    for message in track:
        if message.type in ("note_on", "note_off"):
            # Lower the note until it's in the key.
            while message.note > 0 and message.note not in notes:
                message.note -= 1
            # If we lowered too far, we will have to do the opposite.
            while message.note < 127 and message.note not in notes:
                message.note += 1


def shift_nearest(track: mido.MidiTrack, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes to the nearest note in key.
    """
    # Get the absolute value of the difference between each item in
    # the list and message.note, and pick the smallest amongst them.
    for message in track:
        if message.type in ("note_on", "note_off"):
            message.note = min(notes, key=lambda x: abs(x - message.note))


def correct_pitch(
    source: mido.MidiFile,
    key: midi_abstraction.Key,
    strategy: Callable[[mido.Message], None],
) -> mido.MidiFile:
    """
    Snap pitches to notes in the given key via the strategy.
    """
    # Collect a list of midi pitches that are in the key.
    notes = []
    for n in key.list_notes():
        notes.extend(midi_abstraction.notes(n))

    for track in source.tracks:
        strategy(track, notes)

    return source



