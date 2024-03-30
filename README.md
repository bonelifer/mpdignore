# MPDIgnore
## WIP: May no work currently

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash/)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/bonelifer/mpd-scripts/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)

MPDIgnore is a collection of scripts and configuration files to enhance the functionality of Music Player Daemon (MPD) by providing features such as skipping, ignoring, volume control, playlist management, and playlist monitoring.

## Overview

| File                       | Description                                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------------|
| ignore-skip.py | Python script to ignore or skip the current song in MPD and log the action to a specified file. |
| ignore.sh | Bash script to call the Python script with the 'ignore' argument.                               |
| mpdignore.py | Python script to monitor changes to an MPD ingest playlist and add tracks to a specified file.   |
| install.sh | Bash script to install and configure the MPDIgnore system.                                        |
| config.ini | Configuration file containing MPD server details and paths.                                       |
| skip.sh | Bash script to call the Python script with the 'skip' argument.                                    |
| mpdignore.path | Systemd path unit file to monitor changes to the MPD ingest playlist.                             |
| mpdignore.service | Systemd service unit file to run the `mpdignore.py` script.                                       |

## Usage

To use these scripts, ensure you have the necessary dependencies installed and configure the `config.ini` file with your MPD server details and paths. Then, run the `install.sh` script to set up the MPDIgnore system. You can then use the provided scripts to control various aspects of your MPD server.

## MPDIGNORE Workflow
[WORKFLOW](./DOCS/WORKFLOW.md)

## License

This project is licensed under the **GNU General Public License v3**.

See [LICENSE](./LICENSE) for more information.
