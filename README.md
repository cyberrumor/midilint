# midilint
CLI Midi normalizer

This program reads a .mid file and processes it with various functions, outputting a new midi file.

Features:
- Normalization. Set all notes to a particular velocity.
- Pitch correction. Snap all notes to the specified key.

# Runtime dependencies
```
pip3 install --user -r --break-system-packages requirements.txt
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

For example, to set the velocity of all notes in 'my_file.mid' to 150 and
save it as my_file_normalized.mid:
```
python3 midilint.py --velocity=150 /path/to/my_file.mid /path/to/new/my_file_normalized.mid
```

