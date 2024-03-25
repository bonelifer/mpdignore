#!/usr/bin/env python3
"""
volume.py

Description:
    This script adjusts the volume of an MPD (Music Player Daemon) server based on the command-line argument provided ('up' or 'down').
    It connects to the MPD server using the configuration specified in 'config.ini', authenticates if a password is provided, and then adjusts the volume accordingly.
    Finally, it prints a message indicating the volume change and disconnects from the MPD server.

Usage:
    python volume.py [up | down]

Example:
    python volume.py up
    python volume.py down
"""

import argparse
import configparser
from mpd import MPDClient

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Adjust MPD volume.')
    parser.add_argument('direction', choices=['up', 'down'], help='Direction to adjust volume (up or down)')
    args = parser.parse_args()

    # Read configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    mpd_server = config['MPD']['SERVER']
    mpd_port = int(config['MPD']['MPD_PORT'])
    mpd_pass = config['MPD']['MPDPASS']

    # Connect to MPD server
    client = MPDClient()
    client.connect(mpd_server, mpd_port)

    # Authenticate
    client.password(mpd_pass)

    # Adjust volume based on command-line argument
    try:
        if args.direction == 'up':
            client.volume('+5')  # Increase volume by 5 units
            print("Volume increased by 5 units.")
        elif args.direction == 'down':
            client.volume('-5')  # Decrease volume by 5 units
            print("Volume decreased by 5 units.")
    except Exception as e:
        print(f"Error: {e}")

    # Disconnect from MPD server
    client.close()
    client.disconnect()

if __name__ == "__main__":
    main()

