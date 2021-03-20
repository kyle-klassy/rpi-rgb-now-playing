#!/bin/bash

sudo /home/pi/rpi-rgb-led-matrix/utils/text-scroller -f /home/pi/rpi-rgb-led-matrix/fonts/texgyre-27.bdf -C255,0,0 -s3 -l3 -y7 --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 "NOW PLAYING..."

sudo /home/pi/rpi-rgb-led-matrix/utils/text-scroller -f /home/pi/rpi-rgb-led-matrix/fonts/texgyre-27.bdf -C255,0,0 -s3 -l1 -y7 --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 `cat /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_title.txt`

sudo /home/pi/rpi-rgb-led-matrix/utils/led-image-viewer-original /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 --led-brightness=75 &

export LED_PID=$!
echo $LED_PID

inotifywait -m /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png -e close_write |
    while read dir action; do
        echo "The file '$dir' was changed via '$action'"
        echo "Killing previous album cover"
        echo $LED_PID
        echo `pidof led-image-viewer-original`
        sudo kill -9 `pidof led-image-viewer-original`
        sudo kill -9 `pidof text-scroller`
        
        sudo /home/pi/rpi-rgb-led-matrix/utils/text-scroller -f /home/pi/rpi-rgb-led-matrix/fonts/texgyre-27.bdf -C255,0,0 -s3 -l1 -y7 --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 `cat /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_title.txt`
        sudo /home/pi/rpi-rgb-led-matrix/utils/led-image-viewer-original /home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png --led-gpio-mapping=adafruit-hat-pwm --led-cols=64 --led-rows=64 --led-brightness=75 &

    done

