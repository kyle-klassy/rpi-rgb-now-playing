# rpi-rgb-now-playing
Scripts to run on a raspberry pi to display the album cover of my currently playing song on Spotify. Uses the rpi-rgb-led-matrix repo as a starting point, which is provided here: https://github.com/hzeller/rpi-rgb-led-matrix. Check out `rpi-rgb-now-playing/utils/README.md` to install the necessary libraries for using the `led-image-viewer` utility and check other `README.md` files within the repo for tips on how to mitigate led flashing and other annoyances. 

## Installation and file breakdown
I would suggest cloning this repo into `/home/pi/`. The main bash script is: `rpi-rgb-now-playing/utils/spotify_now_playing.sh`, which runs three separate scripts simultaneously:

1. `rpi-rgb-now-playing/utils/led-image-viewer`: Standalone executable that displays the image `rpi-rgb-now-playing/spotify_now_playing/curr_album_cover.png` onto the led matrix. Compiled using the command `make` while inside `rpi-rgb-now-playing/utils/`, which compiles the executable from the source file `led-image-viewer-refresh.cc`. The source code includes an interrupt handler that receives a SIGALRM, which restarts the display and fetches the updated album cover from the directory. 
2. `rpi-rgb-now-playing/spotify_now_playing/fetch_cover.py`: Contacts my heroku server to get the album cover that my spotify account (username klklassy) is currently playing. The album cover of the current song is written to `rpi-rgb-now-playing/spotify_now_playing/curr_album_cover.png`, replacing any existing file with the same name. To modify this code to use your own Spotify activity, you'll have to create your own activity server (mine is located here: https://github.com/kyle-klassy/spotify-data-fetch). 
3. `rpi-rgb-now-playing/utils/monitor_dir.sh`: Monitors the file `curr_album_cover.png` for any new writes. If a write action was detected, a SIGALRM signal is sent to the led-image-viewer executable. 

## Launch on Startup
When loading this repo onto an rpi, add the line `sudo /home/pi/rpi-rgb-now-playing/utils/spotify_now_playing.sh &` to the end of `/etc/rc.local` (before the exit 0 line) so that the script runs at startup. 
