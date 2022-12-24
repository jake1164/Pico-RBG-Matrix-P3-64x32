# RTC Example
This is an example for getting the time from a NTP server and setting the DS3231 RTC chip.

## NOTE: Requires a Pico W and DS3231

### Setup
Create a settings.toml file. Required settings in settings.toml file are as follows:
* TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
* WIFI_SSID="your ssid"
* WIFI_PASSWORD="yoursupersecretpassword"
* NTP_HOST="0.adafruit.pool.ntp.org"

DO NOT CHECK THE settings.toml file into Source Control, add a .gitignore for settings.toml

### Library
This example uses the adafruit_ntp library to connect to an NTP server and get the time

### RTC Pins
* GP06 - I2C data pin
* GP07 - I2C clock pin

## Resources

### Documentation
Circuitpython getenv() documentation[here](https://docs.circuitpython.org/en/latest/docs/environment.html)
Pico W Example [here](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/create-your-settings-toml-file)
