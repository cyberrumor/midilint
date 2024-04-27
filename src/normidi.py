#!/usr/bin/env python3
import mido
import sys
import argparse
from pathlib import Path


def normalize(source: mido.MidiFile, velocity: int) -> mido.MidiFile:
    """
    Normalize messages in source to input velocity and return source.
    """
    for track in source.tracks:
        for message in track:
            if message.type in ("note_on", "note_off"):
                message.velocity = velocity
    return source


def main(source: Path, dest: Path, velocity: int) -> None:
    """
    Parse source, normalize, save to dest.
    """
    mid = mido.MidiFile(source, clip=True)
    output = normalize(mid, velocity)
    output.save(dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"{Path(__file__).name}",
        description="normalize SOURCE midi file and save it to DEST",
    )

    parser.add_argument("SOURCE", type=Path, help="the midi file to normalize")

    parser.add_argument("DEST", type=Path, help="the name of the output file")

    parser.add_argument(
        "--velocity", type=int, default=127, help="the velocity to set all notes to"
    )

    args = parser.parse_args()

    # Raise FileNotFoundError if SOURCE doesn't exist.
    args.SOURCE.resolve()

    # Ensure DEST doesn't already exist.
    if args.DEST.absolute().exists():
        raise FileExistsError(args.DEST)

    # Validate that velocity is 0-127.
    velocity = args.velocity
    if velocity < 0 or velocity > 127:
        raise ValueError(
            f"velocity was {velocity} but must be between 0 and 127 (inclusive)"
        )

    source = args.SOURCE.absolute()
    dest = args.DEST.absolute()
    main(source, dest, velocity)
