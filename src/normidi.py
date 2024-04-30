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


def shift_up(message: mido.Message, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes up.
    """
    # Raise the note until it's in the key.
    while message.note < 127 and message.note not in notes:
        message.note += 1
    # If we raised it too high, we will have to do the opposite.
    while message.note > 0 and message.note not in notes:
        message.note -= 1


def shift_down(message: mido.Message, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes down.
    """
    # Lower the note until it's in the key.
    while message.note > 0 and message.note not in notes:
        message.note -= 1
    # If we lowered too far, we will have to do the opposite.
    while message.note < 127 and message.note not in notes:
        message.note += 1


def shift_nearest(message: mido.Message, notes: list[int]) -> None:
    """
    Change pitch into the key by shifting notes to the nearest.
    """
    # Get the absolute value of the difference between each item in
    # the list and message.note, and pick the smallest amongst them.
    message.note = min(notes, key=lambda x: abs(x - message.note))


def correct_pitch(
    source: mido.MidiFile,
    key: midi_abstraction.Key,
    strategy: Callable[[mido.Message], None],
) -> mido.MidiFile:
    """
    Snap pitches to notes in the given key by raising pitch, with the
    exception of notes that exceed 126 (limitation of midi), which are
    instead lowered.
    """
    # Collect a list of midi pitches that are in the key.
    notes = []
    for n in key.list_notes():
        notes.extend(midi_abstraction.notes(n))

    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                strategy(message, notes)

    return source


def main(source: Path, dest: Path, args) -> None:
    """
    Parse source, manipulate, save to dest.
    """
    mid = mido.MidiFile(source, clip=True)

    # normalize
    if args.velocity is not None:
        mid = normalize(mid, args.velocity)

    # pitch correction
    if args.key is not None:
        strats = {
            "up": shift_up,
            "down": shift_down,
            "nearest": shift_nearest,
        }
        key = midi_abstraction.Key(args.key)
        mid = correct_pitch(mid, key, strats[args.strategy])

    mid.save(dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"{Path(__file__).name}",
        description="Read SOURCE midi file and save processed version to DEST",
    )

    parser.add_argument("SOURCE", type=Path, help="the midi file to normalize")

    parser.add_argument("DEST", type=Path, help="the name of the output file")

    parser.add_argument("--velocity", type=int, help="the velocity to set all notes to")

    parser.add_argument(
        "--key", type=str, help="the key to snap notes to. E.g. c_major or e_phrygian."
    )

    parser.add_argument(
        "--strategy",
        type=str,
        default="nearest",
        help="note snapping algorithm. 'up', 'down', or 'nearest'",
    )

    args = parser.parse_args()

    # Raise FileNotFoundError if SOURCE doesn't exist.
    args.SOURCE.resolve()

    # Ensure DEST doesn't already exist.
    if args.DEST.absolute().exists():
        raise FileExistsError(args.DEST)

    # Validate that velocity is 0-127.
    if args.velocity is not None:
        if args.velocity < 0 or args.velocity > 127:
            raise ValueError(
                f"velocity was {args.velocity} but must be between 0 and 127 (inclusive)"
            )

    # Validate key
    if args.key is not None:
        keys = []
        for n in midi_abstraction.list_notes():
            for m in midi_abstraction.list_modes():
                keys.append(f"{n}_{m}")
        if args.key not in keys:
            raise ValueError(
                f"key was {args.key} but must be one of:\n{'\n'.join(keys)}"
            )

        # If a key was passed, we need to validate the strategy.
        assert args.strategy in [
            "up",
            "down",
            "nearest",
        ], f"strategy was {args.strategy} but must be one of 'up', 'down', or 'nearest'."

    source = args.SOURCE.absolute()
    dest = args.DEST.absolute()
    main(source, dest, args)
