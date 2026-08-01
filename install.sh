#!/usr/bin/bash

# This script installs and configures the MPDIgnore system.
# It sets up the necessary dependencies, copies the scripts to the appropriate directories,
# configures the systemd service and path units, and ensures everything is properly initialized.

set -e

# Define user and group variables
mpdignore_user="root"
mpdignore_group="root"

# User editable variables
MPDIGNORE_FILE=""
MPDIGNORE_PLAYLIST=""
INGEST_PLAYLIST=""

mpdconf="/etc/mpd.conf"
installdir="/usr/local/sbin"

# Function to parse a key out of the [MPDIGNORE] section of config.ini
parse_config_ini_key() {
    local key="$1"
    awk -F '=' -v key="$key" '/\[MPDIGNORE\]/{f=1} f && $1 ~ key {print $2; exit}' "$HOME/.config/mpdignore/config.ini" | tr -d '[:space:]'
}

# Function to get PLDIR (playlist_directory) from mpd.conf.
# mpd.conf uses `key "value"` syntax, not INI sections.
get_pldir() {
    grep -E '^[[:space:]]*playlist_directory[[:space:]]' "$mpdconf" 2>/dev/null \
        | sed -E 's/^[[:space:]]*playlist_directory[[:space:]]+"([^"]*)".*/\1/' \
        | head -n 1
}

# Function to create MPDIGNORE_FILE
create_mpdignore_file() {
    touch "$MPDIGNORE_FILE"
}

# Function to ensure the python-mpd2 dependency used by ignore-skip.py is available
ensure_python_mpd2() {
    if python3 -c "import mpd" &>/dev/null; then
        return
    fi

    echo "Installing python-mpd2 dependency..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y python3-mpd2
    else
        pip3 install --user python-mpd2
    fi
}

ensure_python_mpd2

mkdir -p "$HOME/.config/mpdignore"
if [[ ! -f "$HOME/.config/mpdignore/config.ini" ]]; then
    cp config.ini.example "$HOME/.config/mpdignore/config.ini"
fi

# Parse config.ini to get the playlist names
MPDIGNORE_PLAYLIST=$(parse_config_ini_key "MPDIGNORE_PLAYLIST")
INGEST_PLAYLIST=$(parse_config_ini_key "INGEST_PLAYLIST")

# Get PLDIR
pldir=$(get_pldir)
if [[ -z "$pldir" ]]; then
    echo "Warning: could not determine playlist_directory from $mpdconf; falling back to /var/lib/mpd/playlists"
    pldir="/var/lib/mpd/playlists"
fi

# Update mpdignore.service with the real install path
sed -i "s|/path/to/mpdignore.py|$installdir/mpdignore.py|" mpdignore.service

# Update mpdignore.path with the real ingest playlist path
sed -i "s|/path/to/ingest/playlist.m3u|$pldir/$INGEST_PLAYLIST|" mpdignore.path

cp ./ignore.sh ./skip.sh ./mpdignore.py ./ignore-skip.py "$installdir"
chown "$mpdignore_user:$mpdignore_group" "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/ignore-skip.py"
chmod +x "$installdir/ignore.sh" "$installdir/skip.sh" "$installdir/mpdignore.py" "$installdir/ignore-skip.py"

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
