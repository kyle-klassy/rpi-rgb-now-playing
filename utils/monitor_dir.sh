#!/bin/bash

inotifywait -m /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png -e close_write |
	while read dir action; do 
		#echo "The file '$dir' was changed via '$action'"
		#echo "Sending reload signal to display script"
		sudo pkill -SIGALRM led-image-viewe 
	done
