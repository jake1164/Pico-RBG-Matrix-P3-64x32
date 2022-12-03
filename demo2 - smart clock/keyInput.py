import board
import digitalio
# The pins we'll use, each will have an internal pullup
keypress_pins = [board.GP15, board.GP19,board.GP21]
# Our array of key objects
key_pin_array = []
# The Keycode sent for each button, will be paired with a control key



# Make all pin objects inputs with pullups
def keyInit():
    for pin in keypress_pins:
        key_pin = digitalio.DigitalInOut(pin)
        key_pin.direction = digitalio.Direction.INPUT
        key_pin.pull = digitalio.Pull.UP
        key_pin_array.append(key_pin)
        
def getKeyValue():
    # Check each pin
    for key_pin in key_pin_array:
        if not key_pin.value:  # Is it grounded?
            keyValue = key_pin_array.index(key_pin)
            return keyValue
