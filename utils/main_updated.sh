#!/bin/bash

(trap 'kill 0' SIGINT; sudo python3 /home/pi/rpi-rgb-now-playing/spotify_now_playing/fetch_cover.py & sudo /home/pi/rpi-rgb-now-playing/utils/updated_new_song.sh)

