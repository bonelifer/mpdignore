#!/bin/bash
# Bash script to call the Python script with the 'skip' argument. 

# Find Python3 executable path
python_path=$(which python3)

if [[ -z "$python_path" ]]; then
    echo "Error: Python3 not found."
    exit 1
fi

# Call Python script with argument
"$python_path" skip-ignore.py skip

