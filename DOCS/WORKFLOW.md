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

1.     Accept user input to determine the action (ignore or skip).
2.     If the action is "ignore":
		*  Add the current track to the INGEST playlist.
		*  Proceed to the next track in the queue.
		* Write the current track to the INGEST playlist.
		* Copy the current queue to a temporary playlist to preserve the playback order.
		* Load the INGEST playlist to add the ignored track without disrupting the current playback.
		* Add the ignored track to the INGEST playlist for queue management.
		* Reload the temporary playlist to restore the original queue.
		* Remove the ignored track from the queue to prevent it from affecting subsequent playback.
		* Proceed to the next track to continue playback seamlessly.
3.     If the action is "skip":
		*  Proceed to the next track in the queue.
		* Log the skipped track.
4.     Repeat the process based on user input.
&nbsp;

## License

This project is licensed under the **GNU General Public License v3**.

See [LICENSE](../LICENSE) for more information.

