#!/usr/bin/env python3
"""
MPD Playlist Viewer

This script connects to an MPD server and displays information about the current song
and the playlist. It also allows for editing the script and pausing execution.

Dependencies:
- os
- sys
- time
- mpd
- configparser

Usage:
python script.py [edit/nano] [optional: offset]

Args:
- "edit" or "nano" to open the script for editing.
- Optionally, specify an offset to adjust the playlist display window.

Example:
python script.py edit 5

Author: [Your Name]
Date: [Date]

"""

import os
import sys
import time
import mpd
import configparser

bold = '\033[1m'
normal = '\033[0m'

def editscript():
    """
    Function to edit the script using nano editor.
    """
    if len(sys.argv) > 1 and sys.argv[1] in ["edit", "nano"]:
        os.system("nano " + os.path.realpath(__file__))
        sys.exit()

def pause(msg):
    """
    Function to pause execution and prompt user with a message.
    
    Args:
    - msg: Message to display when prompting for input.
    """
    input(msg)

def read_config():
    """
    Function to read MPD configuration from config.ini file.
    
    Returns:
    - Dictionary containing MPD configuration.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['MPD']

def main():
    """
    Main function to connect to MPD server, display playlist information, and handle user input.
    """
    mpd_config = read_config()

    client = mpd.MPDClient()
    client.connect(mpd_config['SERVER'], int(mpd_config['MPD_PORT']))
    client.password(mpd_config.get('MPDPASS', ''))

    editscript()

    i = sys.argv[1] if len(sys.argv) > 1 else None

    offset = 10

    if i:
        try:
            i = int(i)
            if 0 < i <= 100:
                offset = i
            else:
                print("Input not a valid number between 1-100; using 10 by default.")
        except ValueError:
            print("Input not a number; using 10 by default.")

    current = client.currentsong()
    plpos = int(client.status()["song"])

    headoffset = offset
    tailoffset = offset

    print("\nCurrent song:")
    print(f"{bold}{current.get('title', 'Unknown')} on {current.get('album', 'Unknown')} by {current.get('artist', 'Unknown')}{normal}\n")

    if plpos - offset <= 0:
        tailoffset = plpos
        print(f"{bold}<< Start of Playlist >>{normal}")

    print("\nPlaylist:")
    playlist = client.playlistinfo()
    for song in playlist[max(0, plpos - offset):min(plpos + offset, len(playlist))]:
        print(f"{song['pos']} {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}")

    print("\nNext up:")
    next_song = playlist[plpos + 1] if plpos + 1 < len(playlist) else None
    if next_song:
        print(f"{next_song['title']} by {next_song['artist']} on {next_song['album']}")
    else:
        print("No more songs in the playlist.")

    client.close()
    client.disconnect()

if __name__ == "__main__":
    main()

