#!/usr/bin/env python3
"""
Music Stats Recorder

This script records statistics about the music library, such as the number and size of files,
and MPD server stats. It appends the data to a file specified in the music library directory.

Dependencies:
- os
- sys
- mpd
- datetime
- pathlib
- subprocess

Usage:
python stats.py [edit/nano] [optional: music_library]

Args:
- "edit" or "nano" to open the script for editing.
- Optionally, specify the music library directory.

Example:
python stats.py edit /path/to/music/library

"""

import os
import sys
import mpd
from datetime import datetime
from pathlib import Path
import subprocess

def editscript():
    scriptname = os.path.realpath(__file__)
    swp = f"{os.path.dirname(scriptname)}/.{os.path.basename(scriptname)}.swp"
    if len(sys.argv) > 1 and sys.argv[1] in ["edit", "nano"]:
        if not os.path.exists(swp):
            subprocess.call(["nano", scriptname])
            exit()
        else:
            print(f"\n{scriptname} is already being edited.")
            print(f"{swp} exists; try fg or look in another window.")
            exit()

def pause(msg):
    input(msg)

editscript()

# Define the music library directory
music_library = "/library/music/"
if len(sys.argv) > 2 and os.path.isdir(sys.argv[2]):
    music_library = sys.argv[2]

stats = os.path.join(music_library, "stats")

mpd_client = mpd.MPDClient()
mpd_client.connect("localhost", 6600)

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(stats, "a") as f:
    f.write(date + "\n")
    f.write(mpd_client.stats() + "\n\n")
    f.write(".flac files found in library:\t{}\t{}\n".format(
        len(list(Path(music_library).rglob("*.flac"))),
        sum(f.stat().st_size for f in Path(music_library).rglob("*.flac"))
    ))
    f.write(".mp3 files found in library: \t{}\t{}\n".format(
        len(list(Path(music_library).rglob("*.mp3"))),
        sum(f.stat().st_size for f in Path(music_library).rglob("*.mp3"))
    ))
    f.write(".opus files found in library: \t{}\t{}\n".format(
        len(list(Path(music_library).rglob("*.opus"))),
        sum(f.stat().st_size for f in Path(music_library).rglob("*.opus"))
    ))
    f.write(".ogg files found in library: \t{}\t{}\n".format(
        len(list(Path(music_library).rglob("*.ogg"))),
        sum(f.stat().st_size for f in Path(music_library).rglob("*.ogg"))
    ))
    f.write(".mp4 files found in library: \t{}\t{}\n".format(
        len(list(Path(music_library).rglob("*.mp4"))),
        sum(f.stat().st_size for f in Path(music_library).rglob("*.mp4"))
    ))

print('-' * os.get_terminal_size().columns)
with open(stats, "r") as f:
    print(f.read())

