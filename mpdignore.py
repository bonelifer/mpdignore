#!/usr/bin/env python3

"""
mpdignore.py

Description:
    This script monitors changes to an MPD ingest playlist and performs the following actions:
    1. Copies new tracks from the ingest playlist to a temporary storage file.
    2. Clears the ingest playlist.
    3. Processes the tracks in the temporary storage file:
       - Adds each track to its respective .mpdignore file in the appropriate album folder.
    4. Empties the temporary storage file once all tracks are processed.

Usage:
    python mpdignore.py
        Monitors changes to the MPD ingest playlist and processes new tracks.

"""

import os
import time
import shutil
import configparser

# Function to read MPD configuration from mpd.conf file
def read_mpd_config():
    """
    Function to read MPD configuration from mpd.conf file.

    Returns:
    - Dictionary containing MPD configuration.
    """
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
            config = {}
            with open(full_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key.strip()] = value.strip()
            return config

    print("MPD configuration file (mpd.conf) not found in common locations.")
    sys.exit(1)

# Load MPD configuration
config = read_mpd_config()
PLDIR = config.get('PLDIR', '/var/lib/mpd/playlists')
MPDIGNORE_PLAYLIST = 'mpdignore.m3u'
MPDIGNORE_FILE = os.path.join(PLDIR, MPDIGNORE_PLAYLIST)
INGEST_PLAYLIST = 'ingest.m3u'

def process_tracks():
    # Process tracks in the temporary storage file
    with open(MPDIGNORE_FILE, 'r') as temp_file:
        for track in temp_file:
            track = track.strip()
            # Extract album folder from the track path
            album_folder = os.path.dirname(track)
            # Construct .mpdignore file path
            mpdignore_path = os.path.join(album_folder, '.mpdignore')
            # Append the track to the .mpdignore file
            with open(mpdignore_path, 'a') as mpdignore_file:
                mpdignore_file.write(track + '\n')

    # Clear the temporary storage file
    open(MPDIGNORE_FILE, 'w').close()

def main_loop():
    while True:
        # Check for changes to the ingest playlist
        if os.path.exists(INGEST_PLAYLIST):
            # Copy new tracks from ingest playlist to temporary storage file
            shutil.copyfile(INGEST_PLAYLIST, MPDIGNORE_FILE)
            # Clear the ingest playlist
            open(INGEST_PLAYLIST, 'w').close()
            # Process the tracks in the temporary storage file
            process_tracks()
        # Wait for changes every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main_loop()

