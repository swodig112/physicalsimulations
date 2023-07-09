#!/usr/bin/env python3
import time as t
import pygame as pg
import numpy as np
pg.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
RESIZABLE = False
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
SOURCE_VELOCITY = 50
WAVE_VELOCITY = 50

class Source:
    def __init__(self, pos, velocity, crtime, color=(255, 255, 255)):
        self.pos = pos
        self.velocity = velocity
        self.creationtime = crtime
        self.color = color

    def draw(self, time, surface):
        pg.draw.circle(surface, self.color, self.pos, WAVE_VELOCITY * (time - self.creationtime), 1)


sources = []
display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
if not RESIZABLE:
    display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


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
    if tc % FPS == 0:
        sources.append(Source((SOURCE_VELOCITY * t + 100, 400), 0, t))
    pg.draw.circle(display, (255, 0, 0), (SOURCE_VELOCITY * t + 100, 400), 5)
    for s in sources:
        s.draw(t, display)
    pg.display.update()
    clock.tick(FPS)
    # The next three lines save screenshots of every frame to the disk
    # After saving them you can use ffmpeg to make a video
    # pg.image.save(display, "pngs/{0}.png".format(tc))
    # if t >= 10:
    #     exit()
