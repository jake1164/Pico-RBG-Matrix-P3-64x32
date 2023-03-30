import time
from math import sin
import board
import displayio
import rgbmatrix
import framebufferio
import adafruit_imageload
import terminalio
from adafruit_display_text.label import Label

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 2
tile_down = 1
serpentine = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

display.rotation = 180

g = displayio.Group()
b, p = adafruit_imageload.load("images/ws.bmp")
#b, p = adafruit_imageload.load("pi-logo32b.bmp")
#b, p = adafruit_imageload.load("wales_32x64.bmp")
t = displayio.TileGrid(b, pixel_shader=p)
t.x = 15
#t.x = 0
g.append(t)

l = Label(text="Waveshare\nRGB Matrix", font=terminalio.FONT, color=0xffffff, line_spacing=.7)
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
