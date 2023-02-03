# Thanks to: 2021 Kattni Rembor for Adafruit Industries
# 2023 Kris Swanson, CW, SH, NB - Pine Crest Boca iLab
"""
Example using create_and_get_feed. Creates a new feed if it does not exist and sends to it, or
sends to an existing feed once it has been created.
"""
import ssl
import adafruit_requests
import socketpool
import wifi
import microcontroller
import analogio
from adafruit_io.adafruit_io import IO_HTTP
import board
from time import sleep

analog_pin = analogio.AnalogIn(board.A0)

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials, and "aio_username" and "aio_key" keys with your
# Adafruit IO credentials, DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print(
        "WiFi and Adafruit IO credentials are kept in secrets.py, please add them there!"
    )
    raise

# Connect to Wi-Fi using credentials from secrets.py
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to {}!".format(secrets["ssid"]))
print("IP:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Obtain Adafruit IO credentials from secrets.py
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)


while True:
    
    elapsedTime = 0
    flexHigh = 0
    flexLow = 7000
    while elapsedTime < 10:
        
        flexValue = (analog_pin.value - 37000)
        print("Current FlexValue: {0}".format(flexValue))
        if flexValue > flexHigh:
            flexHigh = flexValue
            
        if flexValue < flexLow:
            flexLow = flexValue
                
        elapsedTime = elapsedTime + .05
        sleep(.05)        

    # Create and get feed.
    io.send_data(io.create_and_get_feed("dogbrace.10sec-high")["key"], flexHigh)
    io.send_data(io.create_and_get_feed("dogbrace.10sec-low")["key"], flexLow)
