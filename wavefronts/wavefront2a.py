#!/usr/bin/env python3
import time as t
import pygame as pg
import numpy as np
pg.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
RESIZABLE = False
FPS = 30
BACKGROUND_COLOR = (0, 0, 0)
O = np.array([100, WINDOW_HEIGHT // 2])
SOURCE_VELOCITY = 40
WAVE_VELOCITY = 50
LAMBDA = 50
AMPLITUDE = 1
ANGULAR_WAVE_NUMBER = 2 * np.pi / LAMBDA
ANGULAR_FREQUENCY = ANGULAR_WAVE_NUMBER * WAVE_VELOCITY

def f(x, m, o, k, t): # The Wave Function
    return m * np.cos(k * x - o * t)


class Source:
    def __init__(self, pos, velocity, creationtime, destroytime, color=(255, 255, 255)):
        self.pos = pos
        self.velocity = velocity
        self.creationtime = creationtime
        self.destroytime = destroytime
        self.color = np.array(color)

    def draw(self, time, surface):
        if time < self.creationtime:
            return
        for r in range(int((time - self.destroytime) * self.velocity), int((time - self.creationtime) * self.velocity) + 1):
            pg.draw.circle(surface, (self.color * (f(r, 1, ANGULAR_FREQUENCY, ANGULAR_WAVE_NUMBER, t) + 1) / 2).astype(np.uint8), self.pos, r, 1)


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
    if tc % 10 == 0:
    # if tc == 10:
        sources.append(Source((SOURCE_VELOCITY * t + 300, 400), WAVE_VELOCITY, t, t + 1))
    pg.draw.circle(display, (255, 0, 0), (SOURCE_VELOCITY * t + 100, 400), 5)
    for s in sources:
        # print("HERE")
        s.draw(t, display)
    pg.display.update()
    clock.tick(FPS)
    # The next three lines save screenshots of every frame to the disk
    # After saving them you can use ffmpeg to make a video
    # pg.image.save(display, "pngs/{0}.png".format(tc))
    # if t >= 10:
    #     exit()
