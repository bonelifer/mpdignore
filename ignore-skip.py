#!/usr/bin/env python3

"""
This script provides functionality to either ignore or skip the current song in an MPD playlist.
When invoked with the 'ignore' argument, it adds the current song to a special '.mpdignore.m3u' playlist,
effectively ignoring it for future playback. When invoked with the 'skip' argument, it logs the skipped song
and proceeds to the next song in the playlist.
"""

import subprocess
import datetime
import configparser
import sys
import os

def logsong(mpdlog, current_song):
    timestamp = datetime.datetime.now().strftime('%b %d %H:%M')
    log_entry = f'{timestamp} : player: skipped "{current_song}"\n'
    with open(mpdlog, 'a') as log_file:
        log_file.write(log_entry)

def mpc(args, password, server, port):
    command = ['mpc', '-h', server, '-p', port, '-P', password] + args
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: ./ignore-skip.py <ignore|skip>")
        sys.exit(1)

    action = sys.argv[1]
    config_file = 'config.ini'

    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_file)

    server = config.get('MPD', 'SERVER')
    port = config.get('MPD', 'MPD_PORT')
    password = config.get('MPD', 'MPDPASS')
    pldir = config.get('MPD', 'PLDIR')
    mpdlog = config.get('MPD', 'MPDLOG')

    current_song = mpc(['current', '-f', '%file%'], password, server, port)
    
    if action == 'ignore':
        # Ignore current song
        with open(f"{pldir}/.mpdignore.m3u", 'a') as ignore_file:
            ignore_file.write(current_song + '\n')
    elif action == 'skip':
        # Log and skip
        logsong(mpdlog, current_song)
        mpc(['next'], password, server, port)

if __name__ == "__main__":
    main()

