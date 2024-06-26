# midilint

Transpose, normalize, and align midi notes.


Features:
- Normalization. Set all notes to a particular velocity.
- Pitch correction. Snap all notes to the specified key.
  This is naive and not the same as transposing.
- Transposition. Transpose your song from any canonical key
  to any other key based off scale degrees.
- Align notes to intervals. Snap the start and end of notes
  to quarter note intervals or smaller depending on desired
  precision.


# Usage

```
usage: midilint [-h] [--velocity INT] [--snap KEY] [--transpose KEY] [--align INT] [--info] SOURCE [DEST]

The midi linter.

positional arguments:
  SOURCE           the midi file to lint
  DEST             the name of the output file

options:
  -h, --help       show this help message and exit
  --velocity INT   the velocity to set all notes to
  --snap KEY       the key to snap notes to. E.g. c_major or e_phrygian.
  --transpose KEY  the key to transpose to. E.g. c_major or e_phrygian.
  --align INT      align the start and end of notes to intervals. 1 is quarter note, 2 is eighth, 4 is sixteenth, etc
  --info           read information about a file
```

# Installation

Install Python 3.10 or newer for your operating system. Mac users can install brew, then install
python with that. Windows users can use the download and run the installer from
[python.org](https://www.python.org/downloads/windows/).

```
# Use git to clone this repo then cd into the clone dir.
git clone https://github.com/cyberrumor/midilint
cd midilint

# Install pip if you don't already have it. This is python's package manager.
python -m ensurepip --user --break-system-packages --upgrade
python -m pip install --user --break-system-packages --upgrade pip

# Install build and run requirements.
pip3 install --user -r --break-system-packages requirements.txt

# Install midilint
pip3 install --user --break-system-packages .

# Add your python's user-local bin directory to your PATH, then restart your terminal.
# The method by which you achieve this depends on your operating system.
```

