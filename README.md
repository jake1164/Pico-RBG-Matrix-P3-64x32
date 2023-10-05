# Pico-RBG-Matrix-P3-64x32
This is the example micropython code for the [Waveshare Pico RGB Matrix Clock](https://www.waveshare.com/wiki/Pico-RGB-Matrix-P3-64x32). This version has been modified to be easier to understand by removing some unnecessary code. 

## Clock
If you are just looking for the clock firmware checkout the following:
* [Clock with Open Weather Map Data](https://github.com/jake1164/Pico-RGB-Matrix-Weather-Clock)
* [Clock with Tempest Weather Data](https://github.com/jake1164/tempest-led-weather-clock)

## Requirements
The samples require using CircuitPython and some Adafruit CircuitPython libraries.

### CircuitPython Version 8.x.x
This demo source has been updated to use CircuitPython 8.x.x. Download the latest 8.x.x version to install:

To install download the latest 8.x.x version:

* [pico](https://circuitpython.org/board/raspberry_pi_pico/)
* [pico W](https://circuitpython.org/board/raspberry_pi_pico_w/)

### Libraries
Circuit libraries are included in the lib folder, just copy them to the pico. To update them you need to download the Adafruit 8.x-mpy Bundle from [here](https://circuitpython.org/libraries) and update the specific libraries required by the sample code. 

### Documents
The schematics for this are included in the documents folder for reference. 

### Changes
* Added RTC demo
* Removed block of unused code from demo files making them easier to understand
* Switched rotation to display correct rotation
* Added Light Sensor demo
* Added shameless plug for other projects
