#!/usr/bin/env python3

"""
ignore-skip.py

Description:
    This script provides functionality to either ignore or skip the current song in an MPD playlist.
    When invoked with the 'ignore' argument, it adds the current song to a special '.mpdignore.m3u' playlist,
    effectively ignoring it for future playback. When invoked with the 'skip' argument, it logs the skipped song
    and proceeds to the next song in the playlist.

"""

import subprocess
import datetime
import configparser
import os
import sys

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

def logsong(mpdlog, current_song):
    # Log skipped song
    timestamp = datetime.datetime.now().strftime('%b %d %H:%M')
    log_entry = f'{timestamp} : player: skipped "{current_song}"\n'
    with open(mpdlog, 'a') as log_file:
        log_file.write(log_entry)

def mpc(args, password, server, port):
    # Run mpc command with provided arguments
    command = ['mpc', '-h', server, '-p', port, '-P', password] + args
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: ./ignore-skip.py <ignore|skip>")
        sys.exit(1)

    action = sys.argv[1]

    # Read MPD configuration from mpd.conf
    config = read_mpd_config()

    server = config.get('MPD', 'SERVER')
    port = config.get('MPD', 'MPD_PORT')
    password = config.get('MPD', 'MPDPASS')
    pldir = config.get('MPD', 'PLDIR')
    mpdlog = config.get('MPD', 'MPDLOG')

    current_song = mpc(['current', '-f', '%file%'], password, server, port)

    if action == 'ignore':
        # Add current song to the ingest playlist
        mpc(['add', current_song], password, server, port)
        # Proceed to the next track in the queue
        mpc(['next'], password, server, port)
        # Log the ignored track
        logsong(mpdlog, current_song)
    elif action == 'skip':
        # Log the skipped track
        logsong(mpdlog, current_song)
        # Proceed to the next track in the queue
        mpc(['next'], password, server, port)

if __name__ == "__main__":
    main()

