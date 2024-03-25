#!/bin/bash

# Bash script to execute the Python script 'ignore-skip.py' with the 'ignore' argument,
# which adds the current song to a special '.mpdignore.m3u' playlist to ignore it for future playback.


# Find Python3 executable path
python_path=$(which python3)

if [[ -z "$python_path" ]]; then
    echo "Error: Python3 not found."
    exit 1
fi

# Call Python script with argument
"$python_path" skip-ignore.py ignore

