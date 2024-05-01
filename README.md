# midilint

Transposes, normalizes, and aligns midi notes.


Features:
- Normalization. Set all notes to a particular velocity.
- Pitch correction. Snap all notes to the specified key.
  This is naive and not the same as transposing.

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

# Usage

```
usage: midilint.py [-h] [--velocity VELOCITY] [--key KEY] [--strategy STRATEGY] SOURCE DEST

Read SOURCE midi file and save processed version to DEST

positional arguments:
  SOURCE               the midi file to normalize
  DEST                 the name of the output file

options:
  -h, --help           show this help message and exit
  --velocity VELOCITY  the velocity to set all notes to
  --key KEY            the key to snap notes to. E.g. c_major or e_phrygian.
  --strategy STRATEGY  note snapping algorithm. 'up', 'down', or 'nearest'
```

