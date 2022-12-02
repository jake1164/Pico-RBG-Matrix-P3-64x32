import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label
from digitalio import DigitalInOut, Direction
displayio.release_displays()

# send register
R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=6,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False,rotation=180)



g = displayio.Group()
b, p = adafruit_imageload.load("images/pi-logo32b.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 20
g.append(t)

l = Label(text="Feather\nRP2040", font=terminalio.FONT, color=0xffffff, line_spacing=.7)
g.append(l)

display.show(g)

target_fps = 50
ft = 1/target_fps
now = t0 = time.monotonic_ns()
deadline = t0 + ft

p = 1
q = 17
while True:
    tm = (now - t0) * 1e-9
    x = l.x - 1
    if x < -40:
        x = 63
    y =  round(12 + sin(tm / p) * 6)
    l.x = x
    l.y = y
    display.refresh(target_frames_per_second=target_fps, minimum_frames_per_second=0)
    while True:
        now = time.monotonic_ns()
        if now > deadline:
            break
        time.sleep((deadline - now) * 1e-9)
    deadline += ft
