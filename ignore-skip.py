#!/usr/bin/env python3

"""
Ignore Skip

This script provides functionality to either ignore or skip the current song in an MPD playlist.
When invoked with the 'ignore' argument, it adds the current song to an INGEST playlist,
which is then processed by another script (mpdignore.py) to handle the ignored tracks.
When invoked with the 'skip' argument, it logs the skipped song and proceeds to the next song in the playlist.

Workflow:
- Read MPD configuration from the mpd.conf file.
- Accept user input to determine the action (ignore or skip).
- If the action is "ignore":
    - Add the current track to the INGEST playlist.
    - Proceed to the next track in the queue.
    - Write the current track to the INGEST playlist.
    - Copy the current queue to a temporary playlist to preserve the playback order.
    - Load the INGEST playlist to add the ignored track without disrupting the current playback.
    - Add the ignored track to the INGEST playlist for queue management.
    - Reload the temporary playlist to restore the original queue.
    - Remove the ignored track from the queue to prevent it from affecting subsequent playback.
    - Proceed to the next track to continue playback seamlessly.
- If the action is "skip":
    - Proceed to the next track in the queue.
    - Log the skipped track.
- Repeat the process based on user input.
"""

import subprocess
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

# Temporary playlist path
TEMP_PLAYLIST = os.path.join(PLDIR, "temp_queue")

# Function to copy current track to memory
def copy_current_track_to_memory(current_track):
    with open(TEMP_PLAYLIST, 'w') as temp_file:
        temp_file.write(current_track)

# Function to write queue to TEMP_PLAYLIST
def write_queue_to_temp():
    shutil.copyfile(MPDIGNORE_FILE, TEMP_PLAYLIST)

# Function to load INGEST_PLAYLIST
def load_ingest_playlist():
    shutil.copyfile(INGEST_FILE, MPDIGNORE_FILE)
    open(INGEST_FILE, 'w').close()

# Function to write current track to INGEST_PLAYLIST
def write_current_track_to_ingest(current_track):
    with open(INGEST_FILE, 'w') as ingest_file:
        ingest_file.write(current_track)

# Function to save INGEST_PLAYLIST
def save_ingest_playlist():
    shutil.copyfile(MPDIGNORE_FILE, INGEST_FILE)

# Function to reload TEMP_PLAYLIST
def reload_temp_playlist():
    shutil.copyfile(TEMP_PLAYLIST, MPDIGNORE_FILE)

# Function to advance to next track
def advance_to_next_track():
    # Remove current track from TEMP_PLAYLIST
    with open(TEMP_PLAYLIST, 'r') as temp_file:
        next_track = temp_file.readline()
        next_track = temp_file.readline()
    reload_temp_playlist()
    return next_track.strip()

# Main loop
def main_loop():
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main_loop()

