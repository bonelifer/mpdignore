#!/bin/bash

# This script installs and configures the MPDIgnore system.
# It sets up the necessary dependencies, copies the scripts to the appropriate directories,
# configures the systemd service and path units, and ensures everything is properly initialized.

# Define user and group variables
mpdignore_user="root"
mpdignore_group="root"

# User editable variables
MPDIGNORE_FILE=""
MPDIGNORE_PLAYLIST=""

mpdconf="/etc/mpd.conf"
installdir="/usr/local/sbin"

# Function to parse config.ini and retrieve the value of MPDIGNORE_PLAYLIST
parse_config_ini() {
    awk -F '=' '/\[MPDIGNORE\]/{f=1} f && /MPDIGNORE_PLAYLIST/{print $2; exit}' "$HOME/.config/config.ini" | tr -d '[:space:]'
}

# Function to get PLDIR from mpd.conf
get_pldir() {
    awk -F '=' '/\[MPD\]/{f=1} f && /PLDIR/{print $2; exit}' "$mpdconf" | tr -d '[:space:]'
}

# Function to create MPDIGNORE_FILE
create_mpdignore_file() {
    touch "$MPDIGNORE_FILE"
}

# Update mpdignore.service
sed -i "s|/path/to/|$installdir|" mpdignore.service

# Update mpdignore.path
pldir=$(get_pldir)
sed -i "s|/path/to/|$pldir|" mpdignore.path

cp config.ini "$HOME/.config/"
cp ./ignore.sh ./skip.sh ./mpdignore.py ./ignore-skip.py "$installdir"
chown "$mpdignore_user:$mpdignore_group" "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/ignore-skip.py"
chmod +x "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/ignore-skip.py"


# Parse config.ini to get MPDIGNORE_PLAYLIST
MPDIGNORE_PLAYLIST=$(parse_config_ini)

if [[ -f "$mpdconf" ]]; then
   # If mpd.conf exists in the specified location
   found_conf="$mpdconf"
   mpdpass="$(grep -v "^#" "$mpdconf" | grep -v "^$" | grep password | grep control | head -n 1)"
   mpdpass="${mpdpass%*\"}"
   mpdpass="${mpdpass#*\"}"
   mpdpass="${mpdpass%\@*}"
fi

# Get PLDIR
pldir=$(get_pldir)

# Create MPDIGNORE_FILE path
MPDIGNORE_FILE="$pldir/$MPDIGNORE_PLAYLIST"

# Create MPDIGNORE_FILE
create_mpdignore_file

# Print MPDIGNORE_FILE path
echo "MPDIGNORE_FILE: $MPDIGNORE_FILE"



if [[ ! -L "$installdir/skip" ]]; then
 ln -s "$installdir/skip.sh" "$installdir/skip"
fi

if [[ ! -L  "$installdir/ignore" ]]; then
 ln -s "$installdir/ignore.sh" "$installdir/ignore"
fi

sudo cp mpdignore.service /etc/systemd/system/
sudo cp mpdignore.path /etc/systemd/system/
sudo chown root:root /etc/systemd/system/mpdignore.path /etc/systemd/system/mpdignore.service 
sudo systemctl daemon-reload
sudo systemctl enable mpdignore.path && sudo systemctl start mpdignore.path && sudo systemctl status mpdignore.path

