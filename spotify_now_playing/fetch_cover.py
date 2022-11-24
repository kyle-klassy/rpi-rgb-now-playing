import datetime
import json
import subprocess
import requests
import time
import os
import signal
import sys

# creating a spotify object to get studio albums
client_id = "72232609920f4c0eaee97b78b3bf0168"
client_secret = "2cbe67d7820e410ba89804f8f0f00f0a"
redir_uri = "http://127.0.0.1:8000/userdata/login/"   # dummy redirect application uri, doesn't really matter
refresh = 'AQBlzCWj1YsqCuj8Qo8ZxVVKXYB_dl0Y31TnmP8ttp2ezyE-ULL3NfbjKtG2hDxWfob-ZFI3lJjfV7An5hJXlRz_gJZJVFxbU5OfkGsVnQarnTwkgwa5ErD-idX8ggUfsbE'
REFRESH_URL = "https://spotify-fetch-backend.fly.dev/userdata/refresh/"

# matrix configurations

def spotifyFetch():

    img, artist, song = None, None, None
    curr_song_data = ''

    try: 
        resp = requests.get(url=REFRESH_URL + refresh).json()
        curr_song_data = resp["current_song"]
    except:
        with open("/home/pi/rpi-rgb-now-playing/logs/logfile.txt", "a") as f:
            ct = datetime.datetime.now()
            print(ct, "Caught an exception parsing json (maybe a podcast?)", file=f, flush=True)

    if curr_song_data != '':
        curr_song_data = json.loads(curr_song_data)
        img = curr_song_data["art"]
        artist = curr_song_data["artist"]
        song = curr_song_data["song"]

    return img, artist, song

def main():
    file = None
    image = None
    prev_artist = None
    prev_track = None
    prev_img = None
    curr_display_img = None

    while(True):

        # if parsing fails, spotifyFetch() will return None for all values
        img, artist, track = spotifyFetch()

        # if we got a valid image and we're not currently displaying it on the screen
        if img is not None and img != curr_display_img:

            with open("/home/pi/rpi-rgb-now-playing/logs/logfile.txt", "a") as f:
                ct = datetime.datetime.now()
                print(ct, "NOW DISPLAYING:", artist, "-", track, file=f, flush=True)

            with open("/home/pi/rpi-rgb-now-playing/spotify_now_playing/curr_title.txt", "w") as f:
                print(artist, "-", track, file=f, flush=True)

            image_file = requests.get(img)
            curr_display_img = img

            file = open("/home/pi/rpi-rgb-now-playing/spotify_now_playing/curr_album_cover.png", "wb")
            file.write(image_file.content)
            file.close()
        
        # if we changed tracks but we kept the same album cover
        if prev_img == img and track != prev_track:
            with open("/home/pi/rpi-rgb-now-playing/logs/logfile.txt", "a") as f:
                ct = datetime.datetime.now()
                print(ct, "SAME ALBUM:", artist, "-", track, file=f, flush=True)

            with open("/home/pi/rpi-rgb-now-playing/spotify_now_playing/curr_title.txt", "w") as f:
                print(artist, "-", track, file=f, flush=True)

            image_file = requests.get(img)
            curr_display_img = img
            file = open("/home/pi/rpi-rgb-now-playing/spotify_now_playing/curr_album_cover.png", "wb")
            file.write(image_file.content)
            file.close()

        # if we couldn't parse the json 
        if img is None and prev_img is not None: 
            with open("/home/pi/rpi-rgb-now-playing/logs/logfile.txt", "a") as f:
                ct = datetime.datetime.now()
                print(ct, "Nothing currently playing", file=f, flush=True)
        
        prev_artist = artist
        prev_track = track
        prev_img = img
        
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
