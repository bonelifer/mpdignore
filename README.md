# MPDIgnore

MPDIgnore is a collection of scripts and configuration files to enhance the functionality of Music Player Daemon (MPD) by providing features such as skipping, ignoring, volume control, playlist management, and playlist monitoring.

## Overview

| File                       | Description                                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------------|
| ignore-skip.py | Python script to ignore or skip the current song in MPD and log the action to a specified file. |
| ignore.sh | Bash script to call the Python script with the 'ignore' argument.                               |
| volume.py | Python script to adjust the volume of MPD.                                                       |
| mpdvoldown.py | Python script to decrease the volume of MPD.                                                      |
| mpdignore.py | Python script to monitor changes to an MPD ingest playlist and add tracks to a specified file.   |
| install.sh | Bash script to install and configure the MPDIgnore system.                                        |
| pl.py | Python script to display the current playlist in MPD.                                             |
| mpdvolup.py | Python script to increase the volume of MPD.                                                      |
| config.ini | Configuration file containing MPD server details and paths.                                       |
| skip.sh | Bash script to call the Python script with the 'skip' argument.                                    |
| mpdignore.path | Systemd path unit file to monitor changes to the MPD ingest playlist.                             |
| playlist.py | Python script to display the current playlist in MPD.                                             |
| mpdignore.service | Systemd service unit file to run the `mpdignore.py` script.                                       |
| stats.py | Python script to gather statistics about the music library and MPD.                                 |

## Usage

To use these scripts, ensure you have the necessary dependencies installed and configure the `config.ini` file with your MPD server details and paths. Then, run the `install.sh` script to set up the MPDIgnore system. You can then use the provided scripts to control various aspects of your MPD server.

