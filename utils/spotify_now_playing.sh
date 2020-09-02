#!/bin/bash

(trap 'kill 0' SIGINT; python3 /home/pi/rpi-rgb-led-matrix/spotify_now_playing/fetch_cover.py & sudo /home/pi/rpi-rgb-led-matrix/utils/led-image-viewer /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 --led-brightness=75 & /home/pi/rpi-rgb-led-matrix/utils/monitor_dir.sh)

