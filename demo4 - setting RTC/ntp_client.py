# Requires a settings.toml file with the following
# settings in settings file:
# TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
# WIFI_SSID="your ssid"
# WIFI_PASSWORD="yoursupersecretpassword"
# NTP_HOST="0.adafruit.pool.ntp.org"

import os
import ipaddress
import wifi
import socketpool
import adafruit_ntp
#import rtc
import busio
import board
import adafruit_ds3231
import time
import struct

TZ = os.getenv('TZ_OFFSET')
NTP_HOST = os.getenv('NTP_HOST')
SSID = os.getenv('WIFI_SSID')
PASS = os.getenv('WIFI_PASSWORD')

def get_time():
    wifi.radio.connect(SSID, PASS)
    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=TZ, server=NTP_HOST)    
    return ntp.datetime

i2c = busio.I2C(board.GP7, board.GP6)
rtc = adafruit_ds3231.DS3231(i2c)

time = get_time()
print(time)

# NOTE: This changes the system time so make sure you aren't assuming that time
# doesn't jump.

print(rtc.datetime)
rtc.datetime = time
print(rtc.datetime)

