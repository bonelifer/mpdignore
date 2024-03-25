#!/bin/bash

# This script installs and configures the MPDIgnore system.
# It sets up the necessary dependencies, copies the scripts to the appropriate directories,
# configures the systemd service and path units, and ensures everything is properly initialized.
# Make sure to review and customize the configuration in 'config.ini' before running this script.

mpdconf="/etc/mpd.conf"
installdir="/usr/local/sbin"
MPDIGNORE_FILE=""

# Function to get PLDIR from config.ini
get_pldir() {
    awk -F '=' '/\[MPD\]/{f=1} f && /PLDIR/{print $2; exit}' "$HOME/.config/config.ini" | tr -d '[:space:]'
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

if [[ -f "$mpdconf" ]]; then
   # If mpd.conf exists in the specified location
   found_conf="$mpdconf"
   mpdpass="$(grep -v "^#" "$mpdconf" | grep -v "^$" | grep password | grep control | head -n 1)"
   mpdpass="${mpdpass%*\"}"
   mpdpass="${mpdpass#*\"}"
   mpdpass="${mpdpass%\@*}"
elif [[ -f "$HOME/.mpd/mpd.conf" ]]; then
   # If mpd.conf exists in the default location
   found_conf="$HOME/.mpd/mpd.conf"
   mpdpass="$(grep -v "^#" "$HOME/.mpd/mpd.conf" | grep -v "^$" | grep password | grep control | head -n 1)"
   mpdpass="${mpdpass%*\"}"
   mpdpass="${mpdpass#*\"}"
   mpdpass="${mpdpass%\@*}"
elif [[ -f "$HOME/.config/mpd/mpd.conf" ]]; then
   # If mpd.conf exists in an alternative location
   found_conf="$HOME/.config/mpd/mpd.conf"
   mpdpass="$(grep -v "^#" "$HOME/.config/mpd/mpd.conf" | grep -v "^$" | grep password | grep control | head -n 1)"
   mpdpass="${mpdpass%*\"}"
   mpdpass="${mpdpass#*\"}"
   mpdpass="${mpdpass%\@*}"
elif [[ -f "$HOME/.config/mpd.conf" ]]; then
   # If mpd.conf exists in another possible alternative location
   found_conf="$HOME/.config/mpd.conf"
   mpdpass="$(grep -v "^#" "$HOME/.config/mpd.conf" | grep -v "^$" | grep password | grep control | head -n 1)"
   mpdpass="${mpdpass%*\"}"
   mpdpass="${mpdpass#*\"}"
   mpdpass="${mpdpass%\@*}"
fi

if [[ -n "$mpdpass" ]]; then
   # If password is found in any mpd.conf file, update config.ini
   found_config_ini="$HOME/.config/config.ini"
   if [[ -f "$found_config_ini" ]]; then
      sed -i "s/^\(MPDPASS\s*=\s*\).*\$/\1$mpdpass/" "$found_config_ini"
   fi
else
   # If none of the standard locations exist or password not found, prompt the user for the mpd control password
   read -p "What is the mpd control password? " mpdpass
   # Update config.ini with the password entered by the user
   found_config_ini="$HOME/.config/config.ini"
   if [[ -f "$found_config_ini" ]]; then
      sed -i "s/^\(MPDPASS\s*=\s*\).*\$/\1$mpdpass/" "$found_config_ini"
   fi
fi

if [[ -n "$found_conf" ]]; then
   # Update the found configuration file with the password
   sed -i "s/^\(password\s*=\s*\).*\$/\1$mpdpass/" "$found_conf"
fi

# Get PLDIR
pldir=$(get_pldir)

# Create MPDIGNORE_FILE path
MPDIGNORE_FILE="$pldir/.mpdignore.m3u"

# Create MPDIGNORE_FILE
create_mpdignore_file

# Print MPDIGNORE_FILE path
echo "MPDIGNORE_FILE: $MPDIGNORE_FILE"

cp ./config.ini ./stats.py ./mpdvoldown.py ./mpdvolup.py ./pl.py ./playlist.py ./ignore.sh ./skip.sh ./volume.py ./mpdignore.py "$installdir"
chown root:root "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/stats.py" "$installdir/mpdvoldown.py" "$installdir/mpdvolup.py" "$installdir/pl.py" "$installdir/playlist.py" "$installdir/volume.py"
chmod +x "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/stats.py" "$installdir/mpdvoldown.py" "$installdir/mpdvolup.py" "$installdir/pl.py" "$installdir/playlist.py" "$installdir/volume.py"

chown root:root "$installdir/config.ini"   # Change ownership to root
chmod 600 "$installdir/config.ini"         # Set permissions to allow only root to read and modify

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

