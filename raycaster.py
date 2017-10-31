#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# raycaster-tk
# https://github.com/vesche/raycaster-tk
#

import math
from Tkinter import Tk, Canvas

m = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
      [1,2,1,2,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,2,0,0,0,3,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,1,0,2,0,3,0,2,0,1,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

# constants
WIDTH = 1024
HEIGHT = 768
MOVSPEED = 0.2
ROTSPEED = 0.05

# trig constants
TGM = (math.cos(ROTSPEED), math.sin(ROTSPEED))
ITGM = (math.cos(-ROTSPEED), math.sin(-ROTSPEED))
COS, SIN = 0, -1

# init vars
positionX = 3.0
positionY = 7.0
directionX = 1.0
directionY = 0.0
planeX = 0.0
planeY = 0.66

# init tkinter
root = Tk()
root.title("raycaster-tk")
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

def leftKey(event):
    global directionX
    global directionY
    global planeX
    global planeY
    directionY = directionX * ITGM[SIN] + directionY * ITGM[COS]
    directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
    planeY = planeX * ITGM[SIN] + planeY * ITGM[COS]
    planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]

def rightKey(event):
    global directionX
    global directionY
    global planeX
    global planeY
    directionY = directionX * TGM[SIN] + directionY * TGM[COS]
    directionX = directionX * TGM[COS] - directionY * TGM[SIN]
    planeY = planeX * TGM[SIN] + planeY * TGM[COS]
    planeX = planeX * TGM[COS] - planeY * TGM[SIN]

def upKey(event):
    global positionX
    global positionY
    if not m[int(positionX + directionX * MOVSPEED)][int(positionY)]:
        positionX += directionX * MOVSPEED
    if not m[int(positionX)][int(positionY + directionY * MOVSPEED)]:
        positionY += directionY * MOVSPEED

def downKey(event):
    global positionX
    global positionY
    if not m[int(positionX - directionX * MOVSPEED)][int(positionY)]:
        positionX -= directionX * MOVSPEED
    if not m[int(positionX)][int(positionY - directionY * MOVSPEED)]:
        positionY -= directionY * MOVSPEED

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)

while True:
    canvas.delete('all')

    for x in range(WIDTH):
        mapX = int(positionX)
        mapY = int(positionY)

        cameraX = 2.0 * x / WIDTH - 1.0
        rayDirX = directionX + planeX * cameraX
        rayDirY = directionY + planeY * cameraX + .0000001 # avoid death by ZDE
        deltaDistX = math.sqrt(1.0 + (rayDirY * rayDirY) / ((rayDirX * rayDirX)))
        deltaDistY = math.sqrt(1.0 + (rayDirX * rayDirX) / ((rayDirY * rayDirY)))

        if rayDirX < 0:
            stepX = -1
            sideDistX = (positionX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - positionX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (positionY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - positionY) * deltaDistY

        hit = False
        while not hit:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = False
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = True
            if m[mapX][mapY] > 0:
                hit = True

        if not side:
            perpWallDist = abs((mapX - positionX + (1.0 - stepX) / 2.0) / rayDirX)
        else:
            perpWallDist = abs((mapY - positionY + (1.0 - stepY) / 2.0) / rayDirY)

        lineHeight = abs(int(HEIGHT / (perpWallDist + .0000001))) # avoid death by ZDE again

        drawStart = -lineHeight / 2.0 + HEIGHT / 2.0
        drawEnd = lineHeight / 2.0 + HEIGHT / 2.0
        if drawStart < 0:
            drawStart = 0
        if drawEnd >= HEIGHT:
            drawEnd = HEIGHT - 1

        # colors
        wallcolors = [[], [150,0,0], [0,150,0], [0,0,150]]
        color = wallcolors[m[mapX][mapY]]
        if side:
            for k, v in enumerate(color):
                color[k] = int(v / 1.2)
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])

        canvas.create_line(x, drawStart, x, drawEnd, fill=hex_color)

    # update screen
    root.update()
