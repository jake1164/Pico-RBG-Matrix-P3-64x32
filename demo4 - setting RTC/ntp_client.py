# This example uses the adafruit_ntp library to connect to an NTP server and get the time
# Requires a settings.toml file that is described [here](https://docs.circuitpython.org/en/latest/docs/environment.html)
# Further example is provided [here](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/create-your-settings-toml-file)
# Required settings in settings file are as follows:
# TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
# WIFI_SSID="your ssid"
# WIFI_PASSWORD="yoursupersecretpassword"
# DO NOT CHECK THE settings.toml file into Source Control, add a .gitignore for settings.toml
import os
import ipaddress
import wifi
import socketpool
import adafruit_ntp
import rtc
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

time = get_time()
print(time)

# NOTE: This changes the system time so make sure you aren't assuming that time
# doesn't jump.
rtc.RTC().datetime = time
