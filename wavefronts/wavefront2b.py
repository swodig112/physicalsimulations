#!/usr/bin/env python3
from enum import CONTINUOUS
import time as t
import pygame as pg
import numpy as np
import skimage.draw as skdraw
pg.init()

DURATION            = 10
WINDOW_WIDTH        = 800
WINDOW_HEIGHT       = 600
RESIZABLE           = False
FPS                 = 60
COEFFICIENT         = 3
BACKGROUND_COLOR    = (0, 0, 0)
O                   = np.array([300, WINDOW_HEIGHT // 2])
SOURCE_VELOCITY     = 30
WAVE_VELOCITY       = 40
LAMBDA              = 50
AMPLITUDE           = 1
ANGULAR_WAVE_NUMBER = 2 * np.pi / LAMBDA
ANGULAR_FREQUENCY   = ANGULAR_WAVE_NUMBER * WAVE_VELOCITY


def f(x, m, o, k, t): # The Wave Function
    return m * np.cos(k * x - o * t)


positions:     list = []
creationtimes: list = []
destroytimes:  list = []

for i in range(DURATION * SOURCE_VELOCITY):
    positions.append((i, 0))
    creationtimes.append(i / SOURCE_VELOCITY)
    destroytimes.append((i + 1) / SOURCE_VELOCITY)

display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
if not RESIZABLE:
    display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

realsurf = pg.surfarray.pixels3d(display)
tmpsurf  = np.zeros((realsurf.shape[0], realsurf.shape[1]))


clock = pg.time.Clock()
clock.get_time()
tc = 0
counter = 1
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        elif e.type == pg.KEYDOWN:
            if e.key == 32:
                counter = (counter + 1) % 2
            elif e.unicode == 'q':
                exit()
    tc += counter
    t = tc / FPS
    display.fill(BACKGROUND_COLOR)
    tmpsurf[:, :] = 0
    for i in range(len(positions)):
        for r in range(int((t - destroytimes[i]) * WAVE_VELOCITY), int((t - creationtimes[i]) * WAVE_VELOCITY) + 1):
            tmp = skdraw.circle_perimeter(int(O[0] + positions[i][0]), int(O[1] + positions[i][1]), r, shape=(WINDOW_WIDTH, WINDOW_HEIGHT))
            tmpsurf[tmp] += f(r, 1, ANGULAR_FREQUENCY, ANGULAR_WAVE_NUMBER, t) / COEFFICIENT

    realsurf[:, :, 0] = 255 * (tmpsurf[:, :] + 1) / 2
    realsurf[:, :, 1] = realsurf[:, :, 0]
    realsurf[:, :, 2] = realsurf[:, :, 0]
    realsurf[tmpsurf > 1, 1] = 0
    realsurf[tmpsurf > 1, 2] = 0
    realsurf[tmpsurf < -1, 0] = 0
    realsurf[tmpsurf < -1, 1] = 0

    pg.draw.circle(display, (0, 255, 0), (SOURCE_VELOCITY * t + O[0], O[1]), 5)
    pg.display.update()
    clock.tick(FPS)
    # The next three lines save screenshots of every frame to the disk
    # After saving them you can use ffmpeg to make a video
    # pg.image.save(display, "pngs/{0}.png".format(tc))
    if t >= 10:
        exit()
