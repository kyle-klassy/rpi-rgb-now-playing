# rpi-rgb-now-playing
Scripts to run on a raspberry pi to display the album cover of my currently playing song on Spotify. Uses the rpi-rgb-led-matrix repo as a starting point, which is provided here: https://github.com/hzeller/rpi-rgb-led-matrix. Check out `rpi-rgb-now-playing/utils/README.md` to install the necessary libraries for using the `led-image-viewer` utility and check other `README.md` files within the repo for tips on how to mitigate led flashing and other annoyances.

Use the following commands to install the necessary libgraphicsmagick++ library:
 ```
 sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
make led-image-viewer
```


## Installation and file breakdown
I would suggest cloning this repo into `/home/pi/`. The main bash script is: `rpi-rgb-now-playing/utils/main_updated.sh`, which runs two scripts simultaneously and traps them with a SIGINT handler:

1. `rpi-rgb-now-playing/spotify_now_playing/fetch_cover.py`: Contacts my backend server to get the album cover and song name that my spotify account (username klklassy) is currently playing. The album cover of the current song is written to `rpi-rgb-now-playing/spotify_now_playing/curr_album_cover.png`, replacing any existing file with the same name. The song name and artist is written to `rpi-rgb-now-playing/spotify_now_playing/curr_title.txt`. To modify this code to use your own Spotify activity, you'll have to create your own activity server (mine is located here: https://github.com/kyle-klassy/spotify-data-fetch).
2. `rpi-rgb-now-playing/utils/updated_new_song.sh`: Cycles through the text "NOW PLAYING..." three times, prints the contents of `./spotify_now_playing/curr_title.txt` to the matrix using the `text-scroller` utility, and then displays the current album cover contained in `curr_album_cover.png`. From there, the script monitors the `curr_album_cover.png` file and watches for changes. Upon a change, the `led-image-viewer` process that was displaying the previous album cover is killed, the new artist and song title are displayed via the text scroller process, and the new album cover is displayed. 

## Launch on Startup
When loading this repo onto an rpi, add the line `sudo /home/pi/rpi-rgb-now-playing/utils/main_updated.sh &` to the end of `/etc/rc.local` (before the exit 0 line) so that the script runs at startup.

## Notes for my own reference
**To set the network name and password in headless mode:** Easiest way is to just use the command line GUI `sudo raspi-config`.

**To set a static IP address:** Edit file `/etc/dhcpcd.conf` and fill in the details following the template in the below image 

![image](https://user-images.githubusercontent.com/25966125/203809812-60e4c261-44b7-452b-b085-fff615045a4d.png)

I have traditionally used `192.168.1.88/24` as my IP, with `192.168.1.254` as the DNS and router IP, but it'll change as I move. Use `hostname -I` to confirm that you're connected to a network, and use `ip r | grep default` to get the gateway IP.
