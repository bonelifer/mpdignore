#!/usr/bin/env python3
"""
mpdvoldown.py

Description:
    This script decreases the volume of an MPD (Music Player Daemon) server by a specified amount.
    It connects to the MPD server using the configuration specified in 'config.ini', authenticates if a password is provided, and then decreases the volume by the specified amount.
    Finally, it prints a message indicating the volume change and disconnects from the MPD server.

Usage:
    python mpdvoldown.py [amount]

Arguments:
    amount: The amount by which to decrease the volume. Must be a positive integer.

Example:
    python mpdvoldown.py 10
        Decreases the volume of the MPD server by 10 units.
"""

import configparser
import subprocess
from mpd import MPDClient

def edit_script(scriptname):
    """
    Function to open the script in an editor for editing.
    """
    try:
        subprocess.run(["nano", scriptname])
    except Exception as e:
        print(f"Error: {e}")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    mpd_server = config['MPD']['SERVER']
    mpd_port = int(config['MPD']['MPD_PORT'])
    mpd_pass = config['MPD']['MPDPASS']

    scriptname = __file__

    edit_command = input("Do you want to edit the script? (y/n): ")
    if edit_command.lower() == 'y':
        edit_script(scriptname)

    # Connect to MPD server
    client = MPDClient()
    client.connect(mpd_server, mpd_port)

    # Authenticate
    client.password(mpd_pass)

    # Decrease volume
    try:
        client.volume('-5')  # Decrease volume by 5 units
        print("Volume decreased by 5 units.")
    except Exception as e:
        print(f"Error: {e}")
    
    # Disconnect from MPD server
    client.close()
    client.disconnect()

if __name__ == "__main__":
    main()

