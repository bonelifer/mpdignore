#!/usr/bin/env python3
"""
mpdignore.py

Description:
    This script reads tracks from the ingest playlist and adds them to the MPD (Music Player Daemon) server's ignore list.
    Tracks listed in the ignore are ignored by MPD with queueing files.

Usage:
    python mpdignore.py

Example:
    python mpdignore.py
        Reads tracks from the ingest playlist and adds them to the MPD ignore list.
""" 

import os
import time
import mpd
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

MPD_SERVER = config['MPD']['SERVER']
MPD_PORT = int(config['MPD']['MPD_PORT'])
MPDPASS = config['MPD'].get('MPDPASS', None)  # Password is optional
SERVER_NAME = config['MPD']['SERVER_NAME']
PLDIR = config['MPD']['PLDIR']
MPDIGNORE_FILE = os.path.join(PLDIR, ".mpdignore.m3u")
INGEST_PLAYLIST = MPDIGNORE_FILE  # For clarity

def is_playlist_busy(client, playlist_name):
    """
    Check if the specified playlist is currently being modified (e.g., songs are being added to it).
    """
    status = client.status()
    if 'playlist' in status and status['playlist'] == playlist_name:
        return True
    return False

def copy_playlist_to_working(client):
    # Clear working playlist
    client.clear("working")
    
    # Load contents of ingest playlist to working playlist
    client.load(MPDIGNORE_FILE, "working")

def clear_ingest_playlist(client):
    # Check if ingest playlist is busy (songs are being added to it)
    if is_playlist_busy(client, INGEST_PLAYLIST):
        print("Ingest playlist is busy. Skipping clear operation.")
    else:
        # Clear the ingest playlist
        client.clear(INGEST_PLAYLIST)

def process_working_playlist(client):
    # Process working playlist and add tracks to .mpdignore file
    with open(os.path.join(PLDIR, ".mpdignore"), "a") as f:
        for song in client.playlistinfo("working"):
            # Add logic here to determine if song should be added to .mpdignore
            # For example, you might check metadata or file paths
            # If condition met, write song file path to .mpdignore
            f.write(song['file'] + "\n")

def main_loop():
    client = mpd.MPDClient()
    client.connect(MPD_SERVER, MPD_PORT)
    if MPDPASS:
        client.password(MPDPASS)

    while True:
        # Wait for changes to ingest playlist
        while not os.path.exists(MPDIGNORE_FILE):
            time.sleep(1)
        
        # Copy ingest playlist to working playlist
        copy_playlist_to_working(client)

        # Clear ingest playlist
        clear_ingest_playlist(client)

        # Process working playlist and add tracks to .mpdignore
        process_working_playlist(client)

    client.close()
    client.disconnect()

if __name__ == "__main__":
    main_loop()

