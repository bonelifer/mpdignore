#!/usr/bin/env python3

"""
Ignore Skip

Ignores or skips the currently playing track in an MPD queue.

- 'ignore': adds the current track to the INGEST playlist (an MPD stored
  playlist) so mpdignore.py can pick it up and record it in the
  appropriate album's .mpdignore file, then advances to the next track.
- 'skip': advances to the next track without ignoring it.
"""

import argparse
import configparser
import os
import re
import sys

from mpd import MPDClient


# Function to parse MPD's `key "value"` config format (mpd.conf is not INI syntax)
def parse_mpd_conf(path):
    settings = {}
    with open(path) as conf_file:
        for line in conf_file:
            line = line.split('#', 1)[0].strip()
            match = re.match(r'^(\S+)\s+"(.*)"$', line)
            if match:
                key, value = match.groups()
                settings[key] = value
    return settings


# Function to read MPDIGNORE configuration from config.ini file
def read_mpdignore_config():
    config = configparser.ConfigParser()
    # Look next to this script first (repo checkout), then the installed location.
    config_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'),
        os.path.expanduser('~/.config/mpdignore/config.ini'),
    ]
    config.read(config_paths)
    mpdignore_config = config['MPDIGNORE']

    mpdignore_config.setdefault('MPD_PORT', '6600')
    mpdignore_config.setdefault('MPDPASS', '')
    mpdignore_config.setdefault('MPD_SERVER', 'localhost')

    mpd_conf_paths = [
        "/etc/mpd.conf",
        "/etc/mpd/mpd.conf",
        "/usr/local/etc/mpd.conf",
        "~/.mpdconf",
        "~/.config/mpd/mpd.conf"
    ]

    for path in mpd_conf_paths:
        full_path = os.path.expanduser(path)
        if os.path.isfile(full_path):
            mpd_settings = parse_mpd_conf(full_path)
            mpdignore_config['MPD_PORT'] = mpd_settings.get('port', mpdignore_config['MPD_PORT'])
            password = mpd_settings.get('password', '')
            if password:
                mpdignore_config['MPDPASS'] = password.split('@', 1)[0]
            break

    return mpdignore_config


mpdignore_config = read_mpdignore_config()
INGEST_PLAYLIST = mpdignore_config.get('INGEST_PLAYLIST')
MPD_SERVER = mpdignore_config.get('MPD_SERVER')
MPD_PORT = int(mpdignore_config.get('MPD_PORT'))
MPDPASS = mpdignore_config.get('MPDPASS')


def connect():
    client = MPDClient()
    client.connect(MPD_SERVER, MPD_PORT)
    if MPDPASS:
        client.password(MPDPASS)
    return client


def ignore_current_track(client):
    current = client.currentsong()
    track_file = current.get('file')
    if not track_file:
        print("No track is currently playing.", file=sys.stderr)
        sys.exit(1)

    client.playlistadd(INGEST_PLAYLIST, track_file)
    print(f"Ignored: {track_file}")
    client.next()


def skip_current_track(client):
    current = client.currentsong()
    track_file = current.get('file', '<unknown>')
    print(f"Skipped: {track_file}")
    client.next()


def main():
    parser = argparse.ArgumentParser(description="Ignore or skip the current MPD track.")
    parser.add_argument('action', choices=['ignore', 'skip'], help="Action to perform")
    args = parser.parse_args()

    client = connect()
    try:
        if args.action == 'ignore':
            ignore_current_track(client)
        else:
            skip_current_track(client)
    finally:
        client.close()
        client.disconnect()


if __name__ == "__main__":
    main()
