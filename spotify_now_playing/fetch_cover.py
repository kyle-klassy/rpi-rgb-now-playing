
import json
import subprocess
import requests
import time
import os
import signal
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# creating a spotify object to get studio albums
client_id = "72232609920f4c0eaee97b78b3bf0168"
client_secret = "2cbe67d7820e410ba89804f8f0f00f0a"
redir_uri = "http://127.0.0.1:8000/userdata/login/"   # heroku application url 
refresh = 'AQBlzCWj1YsqCuj8Qo8ZxVVKXYB_dl0Y31TnmP8ttp2ezyE-ULL3NfbjKtG2hDxWfob-ZFI3lJjfV7An5hJXlRz_gJZJVFxbU5OfkGsVnQarnTwkgwa5ErD-idX8ggUfsbE'
REFRESH_URL = "https://spotify-klklassy.herokuapp.com/userdata/refresh/"

# matrix configurations
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.brightness = 90
options.show_refresh_rate = True
options.pwm_dither_bits = 1
options.pwm_bits = 8
options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'


def herokuGET():

    resp = requests.get(url=REFRESH_URL + refresh).json()
    curr_song_data = resp["current_song"]
    img, artist, song = None, None, None

    # print("*****RECEIVED*****", resp)
    if curr_song_data != '':
        curr_song_data = json.loads(curr_song_data)
        img = curr_song_data["art"]
        artist = curr_song_data["artist"]
        song = curr_song_data["song"]
    return img, artist, song

def main():
    curr_url = ""
    file = None
    image = None
    while(True):
        img, artist, track = herokuGET()

        if curr_url != img and img is not None:
            curr_url = img
            print("NOW DISPLAYING:", artist, "-", track)
            image_file = requests.get(curr_url)

            file = open("/home/pi/rpi-rgb-led-matrix/spotify_now_playing/curr_album_cover.png", "wb")
            file.write(image_file.content)
            file.close()
            '''
            image = Image.open("/home/shared_images/curr_album_cover.png")

            # Make image fit our screen.
            image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

            matrix.SetImage(image.convert('RGB'))
            # image.close()
            '''

        if img is None: 
            print("Nothing currently playing")

        # check for new song every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()



'''
function herokuGET() {
    client.get(REFRESH_URL + refresh, function (response) {

        // displaying current track
        var curr_song_data = JSON.parse(response).current_song;

        if (curr_song_data != '') {
            curr_song_data = JSON.parse(curr_song_data)
            var artist = curr_song_data.artist
            var song = curr_song_data.song;
            var art = curr_song_data.art;
            var link = curr_song_data.link;
            document.getElementById('album_img').src = art;
            document.getElementById('album_img').alt = artist + ' - ' + song;
            document.getElementById('artistText').innerHTML = '<b>' + artist + '</b>';
            document.getElementById('songText').innerHTML = song;
            document.getElementById('album_link').href = link;
        }


        // displaying recently listened to songs in scrolling div
        var recent_songs_data = JSON.parse(response).recent_songs;
        recent_songs_data = JSON.parse(recent_songs_data)
        console.log(recent_songs_data[0])

        addingImages(recent_songs_data);

    });

}

'''
