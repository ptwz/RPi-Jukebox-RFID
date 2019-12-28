#!/usr/bin/env python2

import subprocess
import os 
import time
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
print fifo_name

try:
    os.unlink(fifo_name)
except OSError:
    # If it wasnt' there, even better
    pass

os.mkfifo(fifo_name)
os.chmod(fifo_name, 0666)

while True:
    try:
        fifo = open(fifo_name, "r")
        result = fifo.read().strip()
        parts = result.split(" ")
        cmd = commands[parts[0]]
        arguments = [ int(x)  for x in parts[1:] ]
        print (arguments)
        cmd(*arguments)
    except TypeError:
        # Discard commands that did not match the expected syntax. Maybe log it?
        pass
