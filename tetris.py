import sys
import random

import pygame
from pygame.locals import *

pieces = [
    # All pieces should follow http://tetris.wikia.com/wiki/SRS
    # Line Piece
    [
        [(0,1),(1,1),(2,1),(3,1)],
        [(2,0),(2,1),(2,2),(2,3)],
        [(0,2),(1,2),(2,2),(3,2)],
        [(1,0),(1,1),(1,2),(1,3)],
    ],
    # Square
    [
        [(0,0),(0,1),(1,0),(1,1)],
    ],
    
    [
        [(0,0),(1,0),(2,0),(2,1)],
    ],

    # L piece

#   [(0,0),(1,0),(0,0),(0,0)]
]

def rotatepieceCCW():
    global rotation
    if rotation == 0:
        rotation = len(currpiece) - 1
    else:
        rotation = rotation - 1

def rotatepieceCW():
    global rotation
    if rotation == len(currpiece) - 1:
        rotation = 0
    else:
        rotation = rotation + 1

pygame.init()
clock = pygame.time.Clock()

def drawbox(window, x, y):
    pygame.draw.rect(window, colour.white, (x*SCALE, y*SCALE, SCALE, SCALE))



class colour:
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    blue = pygame.Color(0, 0, 255)
## Config Section
SCALE = 16
FPS = 60

board = set()
# List of tuples with X,Y positions.
# There should never be any duplicates.

currpiece = random.choice(pieces)
rotation = 0
currx = 5
curry = 0
window = pygame.display.set_mode((10*SCALE,18*SCALE))
tick = 0
needsreset = False
while True:
    window.fill(colour.black)

    # Draw gridlines
    pixarr = pygame.PixelArray(window)
    for x in range(0, 10*SCALE):    
        for y in range(0, 18*SCALE):
            if x % SCALE == 0 or y % SCALE == 0:
                pixarr[x][y] = colour.blue
    del pixarr

    for piece in board:
        drawbox(window, piece[0], piece[1])
    print(rotation)
    for piece in currpiece[rotation]:
        drawbox(window, piece[0] + currx, piece[1] + curry)

    if tick % 9 == 0:
        curry = curry + 1

    # Collision Detection

    for item in currpiece[rotation]:
        newx = item[0] + currx
        newy = item[1] + curry
        if (newx, newy) in board:
            needsreset = True
        if newy >= 18:
            needsreset = True

    if needsreset:
        for item in currpiece[rotation]:
            board.add((item[0] + currx, item[1] + curry - 1))
        currpiece = random.choice(pieces)
        rotation = 0
        currx = 3
        curry = 0
        for y in range(0, 18):
            canrm = True
            for x in range(0, 10):
                if not((x, y) in board):
                    canrm = False
            if canrm:
                for x in range(0, 10):
                    board.remove((x, y))
                newboard = set()
                for item in board:
                    if item[1] < y:
                        newboard.add((item[0], item[1] + 1))
                    else:
                        newboard.add((item[0], item[1]))
                board = set(newboard)
        needsreset = False

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                canmove = True
                for item in currpiece[rotation]:
                    if currx + item[0]  == 0:
                        canmove = False
                    if (currx + item[0] - 1, curry + item[1]) in board:
                        canmove = False
                if canmove:
                    currx = currx - 1
            if event.key == K_RIGHT:
                canmove = True
                for item in currpiece[rotation]:
                    if currx + item[0] >= 9:
                        canmove = False
                    if (currx + item[0] + 1, curry + item[1]) in board:
                        canmove = False
                if canmove:
                    currx = currx + 1
            if event.key == K_z:
                rotatepieceCCW()
            if event.key == K_x:
                rotatepieceCW()
    tick = tick + 1
    pygame.display.update()
    clock.tick(FPS)
