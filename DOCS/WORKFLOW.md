## Workflow for **mpdignore.py**:

1.     Read MPD configuration from the mpd.conf file.
2.     Continuously monitor changes to the INGEST playlist.
3.     When a change is detected in the INGEST playlist:
		* Copy the new tracks from the INGEST playlist to the MPDIGNORE_FILE.
		- 	Clear the INGEST playlist.
		- 	Process the tracks in the MPDIGNORE_FILE:
				- 	Add each track to its respective .mpdignore file in the appropriate album folder.
				- 	Empty the MPDIGNORE_FILE once all tracks are processed.
4. Repeat the monitoring process indefinitely.

## Workflow for **ignore-skip.py:**

1.     Accept a single command-line argument: `ignore` or `skip`.
2.     Connect to MPD (host/port/password read from `mpd.conf`) via python-mpd2.
3.     If the action is "ignore":
        * Ask MPD for the currently playing track (`currentsong`).
        * Add that track's path to the INGEST playlist via MPD's `playlistadd` command.
        * Advance to the next track (`next`).
4.     If the action is "skip":
        * Advance to the next track (`next`) without recording it anywhere.
5.     `mpdignore.py` (running separately as a daemon) picks up new entries in the
       INGEST playlist and writes them into the appropriate album's `.mpdignore` file.
&nbsp;

## License

This project is licensed under the **GNU General Public License v3**.

See [LICENSE](../LICENSE) for more information.

