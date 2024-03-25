#!/usr/bin/env python3
"""
Playlist Viewer

This script connects to an MPD server and displays the current song along with a portion of the playlist.
It provides functionalities to edit the script, pause execution, and confirm actions.

Dependencies:
- mpd
- os
- sys
- configparser

Usage:
python playlist.py [edit/remote] [optional: offset]

Args:
- "edit" or "nano" to open the script for editing.
- "remote" to check if running on the designated server.
- Optionally, specify an offset to adjust the playlist display window.

Example:
python playlist.py edit 5



"""

import mpd
import os
import sys
import configparser

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

SERVER = config.get("MPD", "SERVER")
MPD_PORT = int(config.get("MPD", "MPD_PORT"))
MPDPASS = config.get("MPD", "MPDPASS")
SERVER_NAME = config.get("MPD", "SERVER_NAME")
SCRIPT_NAME = os.path.realpath(__file__)

# Function to edit the script
def edit_script():
    os.system("nano " + SCRIPT_NAME)
    exit()

# Function to pause execution
def pause():
    input("Press Enter to continue...")

# Function to prompt for confirmation
def confirm(prompt):
    response = input(prompt + " [Y/n]: ").strip().lower()
    return response == "" or response == "y"

# Function to check if running on the designated server
def is_remote():
    return os.uname().nodename != SERVER_NAME

# Function to connect to MPD
def connect_mpd():
    client = mpd.MPDClient()
    client.connect(SERVER, MPD_PORT)
    client.password(MPDPASS)
    return client

# Function to display playlist
def display_playlist(client, offset):
    playlist = client.playlistinfo()
    current_song = client.currentsong()
    current_index = int(current_song.get("pos", 0))

    start_index = max(0, current_index - offset)
    end_index = min(len(playlist), current_index + offset + 1)

    print("\nCurrent Song:")
    print(f"{current_song.get('artist', '')} - {current_song.get('title', '')}")

    print("\nPlaylist:")
    for i, song in enumerate(playlist[start_index:end_index], start=start_index):
        print(f"{i}. {song.get('artist', '')} - {song.get('title', '')}")

# Main function
def main():
    # Command-line argument handling
    if len(sys.argv) > 1:
        if sys.argv[1] in ["edit", "e", "nano"]:
            edit_script()
        elif sys.argv[1] == "remote":
            if is_remote():
                print("Running on a remote server.")
            else:
                print("Running on the designated server.")
            exit()

    # Connect to MPD
    client = connect_mpd()

    # Display playlist
    display_playlist(client, offset=10)

    # Close connection
    client.close()
    client.disconnect()

if __name__ == "__main__":
    main()

