#!/usr/bin/env python2

import subprocess
import os 
import time
import select
from mpd import MPDClient
from mpd.base import ConnectionError
from LEDStrip import LEDStrip


leds = LEDStrip()
leds.startup()

commands = { "STARTUP":  leds.startup,
        "SHUTDOWN": leds.shutdown,
        "VOLUME": leds.volume,
        "SONG": leds.song,
        "FADE_UP_AND_DOWN": leds.fade_up_and_down,
        "CLEAR": leds.clear}

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))

fifo_name = dir_path+"/../led_control"
print("a")
try:
    os.unlink(fifo_name)
except OSError:
    #Maybe the socket already existed, so keep it
    pass

fifo = open(fifo_name, "w+")
os.chmod(fifo_name, 0666)
mpd = MPDClient()
print('dort')
cur_song = 0
last_song = 0
playlist_length = 0

while True:
    # Handle MPD status first
    try:
        time.sleep(.2)
        status = mpd.status()
        print(status)
        if 'playlistlength' in status:
            playlist_length = status['playlistlength']
        if 'song' in status:
            cur_song = status['song']
        else:
            cur_song = None
        if last_song != cur_song and cur_song is not None:
            last_song = cur_song
            leds.song(int(cur_song), int(playlist_length))
    except ConnectionError:
        mpd.connect('localhost', 6600)
    # Get the list sockets which are readable
    result = fifo.readline().strip()
    parts = result.split(" ")
    print(parts)
    if parts:
        try:
            cmd = commands[parts[0]]
            arguments = [ int(x)  for x in parts[1:] ]
            cmd(*arguments)
        except KeyError:
            pass
        except TypeError:
            # Discard commands that did not match the expected syntax. Maybe log it?
            pass
    fifo.seek(0)
    fifo.truncate()
