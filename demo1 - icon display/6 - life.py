import random
import time

import board
import displayio
from digitalio import DigitalInOut, Direction
import framebufferio
import rgbmatrix

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

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
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

display.rotation = 180

# Conway's "Game of Life" is played on a grid with simple rules, based
# on the number of filled neighbors each cell has and whether the cell itself
# is filled.
#   * If the cell is filled, and 2 or 3 neighbors are filled, the cell stays
#     filled
#   * If the cell is empty, and exactly 3 neighbors are filled, a new cell
#     becomes filled
#   * Otherwise, the cell becomes or remains empty
#
# The complicated way that the "m1" (minus 1) and "p1" (plus one) offsets are
# calculated is due to the way the grid "wraps around", with the left and right
# sides being connected, as well as the top and bottom sides being connected.
#
# This function has been somewhat optimized, so that when it indexes the bitmap
# a single number [x + width * y] is used instead of indexing with [x, y].
# This makes the animation run faster with some loss of clarity. More
# optimizations are probably possible.

def apply_life_rule(old, new):
    width = old.width
    height = old.height
    for y in range(height):
        yyy = y * width
        ym1 = ((y + height - 1) % height) * width
        yp1 = ((y + 1) % height) * width
        xm1 = width - 1
        for x in range(width):
            xp1 = (x + 1) % width
            neighbors = (
                old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                old[x   + ym1] +                  old[x   + yp1] +
                old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
            new[x+yyy] = neighbors == 3 or (neighbors == 2 and old[x+yyy])
            xm1 = x

# Fill 'fraction' out of all the cells.
def randomize(output, fraction=0.33):
    for i in range(output.height * output.width):
        output[i] = random.random() < fraction


# Fill the grid with a tribute to John Conway
def conway(output):
    # based on xkcd's tribute to John Conway (1937-2020) https://xkcd.com/2293/
    conway_data = [
        b'  +++   ',
        b'  + +   ',
        b'  + +   ',
        b'   +    ',
        b'+ +++   ',
        b' + + +  ',
        b'   +  + ',
        b'  + +   ',
        b'  + +   ',
    ]
    for i in range(output.height * output.width):
        output[i] = 0
    for i, si in enumerate(conway_data):
        y = output.height - len(conway_data) - 2 + i
        for j, cj in enumerate(si):
            output[(output.width - 8)//2 + j, y] = cj & 1

SCALE = 1
b1 = displayio.Bitmap(display.width//SCALE, display.height//SCALE, 2)
b2 = displayio.Bitmap(display.width//SCALE, display.height//SCALE, 2)
palette = displayio.Palette(2)
tg1 = displayio.TileGrid(b1, pixel_shader=palette)
tg2 = displayio.TileGrid(b2, pixel_shader=palette)
g1 = displayio.Group(scale=SCALE)
g1.append(tg1)
display.show(g1)
g2 = displayio.Group(scale=SCALE)
g2.append(tg2)

# First time, show the Conway tribute
palette[1] = 0xffffff
conway(b1)
display.auto_refresh = True
time.sleep(3)
n = 40

while True:
    # run 2*n generations.
    # For the Conway tribute on 64x32, 80 frames is appropriate.  For random
    # values, 400 frames seems like a good number.  Working in this way, with
    # two bitmaps, reduces copying data and makes the animation a bit faster
    for _ in range(n):
        display.show(g1)
        apply_life_rule(b1, b2)
        display.show(g2)
        apply_life_rule(b2, b1)

    # After 2*n generations, fill the board with random values and
    # start over with a new color.
    randomize(b1)
    # Pick a random color out of 6 primary colors or white.
    palette[1] = (
        (0x0000ff if random.random() > .33 else 0) |
        (0x00ff00 if random.random() > .33 else 0) |
        (0xff0000 if random.random() > .33 else 0)) or 0xffffff
    n = 200
