#!/usr/bin/env python3

"""
MPDIgnore

This script monitors an INGEST playlist in MPD and processes tracks added to it.
When a track is added to the INGEST playlist, it copies the track to a special '.mpdignore.m3u' file
and then adds each track in this file to its respective '.mpdignore' file in the appropriate album folder.
The INGEST playlist is then cleared. This script runs indefinitely, continuously monitoring the INGEST playlist.

Workflow:
- Read MPD configuration from the mpd.conf file.
- Continuously monitor changes to the INGEST playlist.
- When a change is detected in the INGEST playlist:
    - Copy the new tracks from the INGEST playlist to the MPDIGNORE_FILE.
    - Clear the INGEST playlist.
    - Process the tracks in the MPDIGNORE_FILE:
        - Add each track to its respective .mpdignore file in the appropriate album folder.
        - Empty the MPDIGNORE_FILE once all tracks are processed.
- Repeat the monitoring process indefinitely.
"""

import os
import shutil
import time
import configparser


# Function to read MPDIGNORE configuration from config.ini file
def read_mpdignore_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    mpdignore_config = config['MPDIGNORE']

    # Read additional configuration from mpd.conf
    mpd_conf_paths = [
        "/etc/mpd.conf",
        "/etc/mpd/mpd.conf",
        "/usr/local/etc/mpd.conf",
        "~/.mpdconf",
        "~/.config/mpd/mpd.conf"
    ]

    for path in mpd_conf_paths:
        full_path = os.path.expanduser(path)
        if os.path.isfile(full_path):
            mpd_config = configparser.ConfigParser()
            mpd_config.read(full_path)
            mpd_section = mpd_config['MPD']
            mpdignore_config['PLDIR'] = mpd_section.get('PLDIR', '/var/lib/mpd/playlists')
            mpdignore_config['MPD_PORT'] = mpd_section.get('PORT', '6600')
            mpdignore_config['MPDPASS'] = mpd_section.get('PASSWORD', '')
            mpdignore_config['MPD_SERVER'] = mpd_section.get('SERVER', 'localhost')
            break

    return mpdignore_config

# Load MPDIGNORE configuration
mpdignore_config = read_mpdignore_config()
MPDIGNORE_PLAYLIST = mpdignore_config.get('MPDIGNORE_PLAYLIST')
INGEST_PLAYLIST = mpdignore_config.get('INGEST_PLAYLIST')

# Define the path for the playlist directory
PLDIR = os.path.expanduser(mpdignore_config['PLDIR'])

# Define the paths for the playlist files
MPDIGNORE_FILE = os.path.join(PLDIR, MPDIGNORE_PLAYLIST)
INGEST_FILE = os.path.join(PLDIR, INGEST_PLAYLIST)

# Function to process tracks
def process_tracks():
    with open(MPDIGNORE_FILE, 'r') as temp_file:
        for track in temp_file:
            track = track.strip()
            album_folder = os.path.dirname(track)
            mpdignore_path = os.path.join(album_folder, '.mpdignore')
            with open(mpdignore_path, 'a') as mpdignore_file:
                mpdignore_file.write(track + '\n')
    open(MPDIGNORE_FILE, 'w').close()

# Main loop
def main_loop():
    while True:
        if os.path.exists(INGEST_FILE):
            shutil.copyfile(INGEST_FILE, MPDIGNORE_FILE)
            open(INGEST_FILE, 'w').close()
            process_tracks()
        time.sleep(5)

if __name__ == "__main__":
    main_loop()

