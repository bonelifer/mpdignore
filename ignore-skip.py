#!/usr/bin/env python3

"""
This script provides functionality to either ignore or skip the current song in an MPD playlist.
When invoked with the 'ignore' argument, it adds the current song to a special '.mpdignore.m3u' playlist,
effectively ignoring it for future playback. When invoked with the 'skip' argument, it logs the skipped song
and proceeds to the next song in the playlist.

Workflow:
- Copy current track info to memory.
- Write the queue to TEMPPLAYLIST.
- Load INGESTPLAYLIST.
- Write current track info from memory.
- Save INGESTPLAYLIST.
- Reload TEMPPLAYLIST.
- Using info saved in memory, advance to the next track, deleting the old track from the queue.
- Clear the content of current track info and next track info to ready it for the next usage.
"""

import subprocess
import datetime
import os

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


# Function to interact with MPC
def mpc(args, password, server, port):
    command = ['mpc', '-h', server, '-p', port, '-P', password] + args
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: ./ignore-skip.py <ignore|skip>")
        sys.exit(1)

    action = sys.argv[1]

    # Read MPD configuration from mpd.conf file
    mpd_config = read_mpd_config()
    MPD_SERVER = mpd_config.get('MPD_HOST', 'localhost')
    MPD_PORT = mpd_config.get('MPD_PORT', '6600')
    MPDPASS = mpd_config.get('MPD_PASSWORD', '')
    PLDIR = mpd_config.get('MPD_PLAYLIST_DIRECTORY', '~/.mpd/playlists')
    ING_PLAYLIST = mpd_config.get('MPD_INGEST_PLAYLIST', 'ingest')

    # Temporary playlist name
    temp_playlist = "temp_queue"

    if action == 'ignore':
        # Copy current track info to memory
        current_track_info = mpc(['current', '-f', '%file%'], MPDPASS, MPD_SERVER, MPD_PORT)
        # Write the queue to TEMPPLAYLIST
        mpc(['playlist', 'save', temp_playlist], MPDPASS, MPD_SERVER, MPD_PORT)
        # Load INGESTPLAYLIST
        mpc(['load', ING_PLAYLIST], MPDPASS, MPD_SERVER, MPD_PORT)
        # Write current track info from memory
        mpc(['add', current_track_info], MPDPASS, MPD_SERVER, MPD_PORT)
        # Save INGESTPLAYLIST
        mpc(['playlist', 'save', ING_PLAYLIST], MPDPASS, MPD_SERVER, MPD_PORT)
        # Reload TEMPPLAYLIST
        mpc(['load', temp_playlist], MPDPASS, MPD_SERVER, MPD_PORT)
        # Using info saved in memory, find the next track
        next_track_info = mpc(['playlist', 'next'], MPDPASS, MPD_SERVER, MPD_PORT)
        # Using info saved in memory, delete old track from queue
        mpc(['playlist', 'delete', current_track_info], MPDPASS, MPD_SERVER, MPD_PORT)
        # Play the next track
        mpc(['play', next_track_info], MPDPASS, MPD_SERVER, MPD_PORT)
        # Clear the content of current_track_info and next_track_info
        current_track_info = ""
        next_track_info = ""

    elif action == 'skip':
        # Copy current track info to memory
        current_track_info = mpc(['current', '-f', '%file%'], MPDPASS, MPD_SERVER, MPD_PORT)
        # Log the skipped track
        timestamp = datetime.datetime.now().strftime('%b %d %H:%M')
        log_entry = f'{timestamp} : player: skipped "{current_track_info}"\n'
        with open(mpd_config.get('MPDLOG', ''), 'a') as log_file:
            log_file.write(log_entry)
        # Proceed to the next track in the queue
        mpc(['next'], MPDPASS, MPD_SERVER, MPD_PORT)

if __name__ == "__main__":
    main()

