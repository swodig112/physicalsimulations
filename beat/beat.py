#!/usr/bin/env python3
import pygame as pg
import numpy as np
pg.init()

####################################
# You may edit the variables below #
####################################
# Lambda (in pixels)
L1 = 50
L2 = 55
# Color (RGB)
BGC = (0, 0, 0)       # Background Color
C   = (255, 255, 255) # Wave Color
# Magnitude (in pixels)
M1 = 150
M2 = 150
# Velocity (pixels per second)
V  = 80
# Window Size
W   = 1000     # Width
H   = 800      # Height
RES = True     # Set to False if you wish to save screenshots to make a video of
#############################
# Do not edit anything else #
#############################

FPS = 60
K1 = 2 * np.pi / L1
K2 = 2 * np.pi / L2
O1 = K1 * V
O2 = K2 * V

def f(x, m, o, k, t): # The Wave Function
    return m * np.sin(k * x - o * t)


display = pg.display.set_mode((W, H), pg.RESIZABLE)
if not RES:
    display = pg.display.set_mode((W, H))

clock = pg.time.Clock()
clock.get_time()
tc = 0
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
    tc += 1
    t = tc / FPS
    display.fill(BGC)
    y0 = f(0, M1, O1, K1, t) + f(0, M2, O2, K2, t)
    h = display.get_height() // 2
    for x in range(1, 1900):
        y = f(x, M1, O1, K1, t) + f(x, M2, O2, K2, t)
        pg.draw.line(display, C, (x - 1, y0 + h), (x, y + h), 3)
        y0 = y
    pg.display.update()
    clock.tick(FPS)
    # The next three lines save screenshots of every frame to the disk
    # After saving them you can use ffmpeg to make a video
    # pg.image.save(display, "pngs/{0}.png".format(tc))
    # if t >= 10:
        # exit()
