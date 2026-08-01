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
import re
import shutil
import time
import configparser


# Function to parse MPD's `key "value"` config format (mpd.conf is not INI syntax)
def parse_mpd_conf(path):
    settings = {}
    with open(path) as conf_file:
        for line in conf_file:
            line = line.split('#', 1)[0].strip()
            match = re.match(r'^(\S+)\s+"(.*)"$', line)
            if match:
                key, value = match.groups()
                settings[key] = value
    return settings


# Function to read MPDIGNORE configuration from config.ini file
def read_mpdignore_config():
    config = configparser.ConfigParser()
    # Look next to this script first (repo checkout), then the installed location.
    config_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'),
        os.path.expanduser('~/.config/mpdignore/config.ini'),
    ]
    config.read(config_paths)
    mpdignore_config = config['MPDIGNORE']

    mpdignore_config.setdefault('PLDIR', '/var/lib/mpd/playlists')
    mpdignore_config.setdefault('MUSIC_DIR', '/var/lib/mpd/music')
    mpdignore_config.setdefault('MPD_PORT', '6600')
    mpdignore_config.setdefault('MPDPASS', '')
    mpdignore_config.setdefault('MPD_SERVER', 'localhost')

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
            mpd_settings = parse_mpd_conf(full_path)
            mpdignore_config['PLDIR'] = mpd_settings.get('playlist_directory', mpdignore_config['PLDIR'])
            mpdignore_config['MUSIC_DIR'] = mpd_settings.get('music_directory', mpdignore_config['MUSIC_DIR'])
            mpdignore_config['MPD_PORT'] = mpd_settings.get('port', mpdignore_config['MPD_PORT'])
            password = mpd_settings.get('password', '')
            if password:
                mpdignore_config['MPDPASS'] = password.split('@', 1)[0]
            break

    return mpdignore_config

# Load MPDIGNORE configuration
mpdignore_config = read_mpdignore_config()
MPDIGNORE_PLAYLIST = mpdignore_config.get('MPDIGNORE_PLAYLIST')
INGEST_PLAYLIST = mpdignore_config.get('INGEST_PLAYLIST')

# Define the path for the playlist and music directories
PLDIR = os.path.expanduser(mpdignore_config['PLDIR'])
MUSIC_DIR = os.path.expanduser(mpdignore_config['MUSIC_DIR'])

# Define the paths for the playlist files
MPDIGNORE_FILE = os.path.join(PLDIR, MPDIGNORE_PLAYLIST)
INGEST_FILE = os.path.join(PLDIR, INGEST_PLAYLIST)

# Function to process tracks
def process_tracks():
    with open(MPDIGNORE_FILE, 'r') as temp_file:
        tracks = [line.strip() for line in temp_file if line.strip()]

    for track in tracks:
        # Tracks from MPD are stored relative to MUSIC_DIR; os.path.join
        # leaves an already-absolute track path untouched.
        album_folder = os.path.join(MUSIC_DIR, os.path.dirname(track))
        mpdignore_path = os.path.join(album_folder, '.mpdignore')

        existing = set()
        if os.path.isfile(mpdignore_path):
            with open(mpdignore_path, 'r') as existing_file:
                existing = {line.strip() for line in existing_file}

        if track not in existing:
            with open(mpdignore_path, 'a') as mpdignore_file:
                mpdignore_file.write(track + '\n')

    open(MPDIGNORE_FILE, 'w').close()

# Main loop
def main_loop():
    while True:
        if os.path.exists(INGEST_FILE) and os.path.getsize(INGEST_FILE) > 0:
            shutil.copyfile(INGEST_FILE, MPDIGNORE_FILE)
            open(INGEST_FILE, 'w').close()
            process_tracks()
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
