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
    # J piece
    [
        [(0,0),(0,1),(1,1),(2,1)],
        [(1,0),(2,0),(1,1),(1,2)],
        [(0,1),(1,1),(2,1),(2,2)],
        [(1,0),(1,1),(1,2),(0,2)],
    ],
    # L piece
    [
        [(2,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(1,2),(2,2)],
        [(0,1),(1,1),(2,1),(0,2)],
        [(0,0),(1,0),(1,1),(1,2)],
    ],
    # L piece
    [
        [(1,0),(2,0),(0,1),(1,1)],
        [(1,0),(1,1),(2,1),(2,2)],
        [(1,1),(2,1),(0,2),(1,2)],
        [(0,0),(0,1),(1,1),(1,2)],
    ],
    [
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(2,1),(1,2)],
        [(0,1),(1,1),(2,1),(1,2)],
        [(1,0),(0,1),(1,1),(1,2)],
    ],
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

def hextocolor(c):
    return pygame.Color(int(c[0:2],16), int(c[2:4],16), int(c[4:6],16))

class colour:
    # All colours are from base-16.
    black = hextocolor("151515")
    white = hextocolor("f5f5f5")
    blue = hextocolor("6a9fb5")

piececolours = [
    hextocolor("151515"),
    hextocolor("202020"),
    hextocolor("303030"),
    hextocolor("505050"),
    hextocolor("b0b0b0"),
    hextocolor("d0d0d0"),
    hextocolor("e0e0e0"),
    hextocolor("f5f5f5"),
    hextocolor("ac4142"),
    hextocolor("d28445"),
    hextocolor("f4bf75"),
    hextocolor("90a959"),
    hextocolor("75b5aa"),
    hextocolor("6a9fb5"),
    hextocolor("aa759f"),
    hextocolor("8f5536"),
],
## Config Section
SCALE = 16

WIDTH = 10
HEIGHT = 18
FPS = 60
lines = 0
board = set()
softdrop = False
# Hard drop isn't a real hard drop. It drops twice as fast (1G) as a soft drop
# and letting go does not make it stop. A piece reset does, though.

harddrop = False

# List of tuples with X,Y positions.
# There should never be any duplicates.

currpiece = random.choice(pieces)
rotation = 0
currx = 5
curry = 0
window = pygame.display.set_mode((WIDTH*SCALE,HEIGHT*SCALE))
tick = 0
needsreset = False
while True:
    window.fill(colour.black)

    # Draw gridlines
    pixarr = pygame.PixelArray(window)
    for x in range(0, WIDTH*SCALE):    
        for y in range(0, HEIGHT*SCALE):
            if x % SCALE == 0 or y % SCALE == 0:
                pixarr[x][y] = colour.blue
    del pixarr

    for piece in board:
        drawbox(window, piece[0], piece[1])
    for piece in currpiece[rotation]:
        drawbox(window, piece[0] + currx, piece[1] + curry)

    # Increase level speed by 10% every 10 lines scored.
    if softdrop:
        if tick % 2 == 0:
            curry = curry + 1
    elif harddrop:
        curry = curry + 1
    elif tick % int(30 * (.9 ** (lines))) == 0:
        curry = curry + 1

    # Collision Detection

    for item in currpiece[rotation]:
        newx = item[0] + currx
        newy = item[1] + curry
        if (newx, newy) in board:
            needsreset = True
        if newy >= HEIGHT:
            needsreset = True

    if needsreset:
        for item in currpiece[rotation]:
            board.add((item[0] + currx, item[1] + curry - 1))
        currpiece = random.choice(pieces)
        rotation = 0
        currx = 3
        curry = 0
        harddrop = False
        for y in range(0, HEIGHT):
            canrm = True
            for x in range(0, WIDTH):
                if not((x, y) in board):
                    canrm = False
            if canrm:
                for x in range(0, WIDTH):
                    board.remove((x, y))
                newboard = set()
                lines = lines + 1
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
            if event.key == K_DOWN:
                softdrop = True
            if event.key == K_z:
                rotatepieceCCW()
            if event.key == K_x:
                rotatepieceCW()
            elif event.key == K_UP:
                harddrop = True
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                softdrop = False
    tick = tick + 1
    pygame.display.update()
    clock.tick(FPS)
