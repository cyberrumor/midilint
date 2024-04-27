# normidi
CLI Midi normalizer

This program reads a .mid file and sets all note velocities to the specified value.

Note velocities can be 0 through 127 (inclusive).

# Runtime dependencies
```
pip3 install --user -r --break-system-packages requirements.txt
```

# Usage
```
usage: normidi.py [-h] [--velocity VELOCITY] SOURCE DEST

normalize SOURCE midi file and save it to DEST

positional arguments:
  SOURCE               the midi file to normalize
  DEST                 the name of the output file

options:
  -h, --help           show this help message and exit
  --velocity VELOCITY  the velocity to set all notes to
```

For example, to set the velocity of all notes in 'my_file.mid' to 150 and
save it as my_file_normalized.mid:
```
python3 normidi.py --velocity=150 /path/to/my_file.mid /path/to/new/my_file_normalized.mid
```

