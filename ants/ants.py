# -*- coding: utf-8 -*-
"""
/*
 * Software License Agreement (BSD License)
 *
 * Copyright (c) 2019 Oliver Mayer, Akademie der Bildenden Kuenste Nuernberg. 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * - Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 * - Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
 

Implementation of Langton's ant
https://en.wikipedia.org/wiki/Langton%27s_ant

required modules:
    pygame   https://pypi.org/project/pygame/
    numpy    https://pypi.org/project/numpy/
 
"""

import sys
import pygame as pg
import numpy as np
import random
from time import sleep

# Ant class 
# Stores position and handles movement of the ant according to a set of rules
class Ant:

    # Constructor: Specify ant's starting position in the stage with xstart, ystart
    #              and starting direction. 
    #              Directions are 0=left, 1=up, 2=right, 3=down
    def __init__(self, xstart, ystart, direction=3):
        self.x = xstart
        self.y = ystart
        self.dir = direction

    # function to update ant direction and position according on the stage
    def update(self, stage):
    
        # update ant's direction and value of the stage under the ant
        if stage[self.y][self.x] == 0:
            self.dir = (self.dir+1) % 4
            stage[self.y][self.x] = 1
        else:
            if self.dir == 0:
                self.dir = 3
            else:
                self.dir = self.dir-1
            stage[self.y][self.x] = 0

    # function to move ant to new position after updating direction
    def move(self, stage):

        # update ant's position
        if self.dir == 0:    # go to left
            if self.x == 0:
                self.x = stage.shape[1]-1
            else:
                self.x = self.x - 1

        elif self.dir == 1:  # go up
            if self.y == 0:
                self.y = stage.shape[0]-1
            else:
                self.y = self.y - 1

        elif self.dir == 2:  # go right
            self.x = (self.x + 1) % stage.shape[1]

        else:                # go down
            self.y = (self.y + 1) % stage.shape[0]

    # draw ant at it's position with colorA. call after drawing the stage
    def draw(self):
        pg.draw.rect(screen, colorA, (self.x*cellSize, self.y*cellSize, cellSize, cellSize))


# Inverted Ant class derived from Ant class 
# Overrides the Ant class' update function for a new set of rules while using the implementation of
# move and draw functions of Ant class
class InvertedAnt(Ant):

    # constructor. usually calls the constructor of the parent class
    def __init__(self, xstart, ystart, direction=3):
        Ant.__init__(self, xstart, ystart, direction)

    # function to update ant direction inversely to the normal ant.
    # !! Overrides the update function of it's parent class Ant. 
    def update(self, stage):
    
        # update ant's direction and value of the stage under the ant
        if stage[self.y][self.x] == 0:  
            
            if self.dir == 0:
                self.dir = 3
            else:
                self.dir = self.dir-1

            stage[self.y][self.x] = 1
        else:
            self.dir = (self.dir+1) % 4
            
            stage[self.y][self.x] = 0




# draw the stage with color0 for stage value = 0 and color1 for stage value = 1
def drawStage( stageArray ):
    
    screen.fill(color0)
    
    for j in range(0, stageArray.shape[0]):
        for i in range(0, stageArray.shape[1]):
            if stageArray[j][i] == 1:
                pg.draw.rect(screen, color1, (i*cellSize, j*cellSize, cellSize, cellSize))
    return   

       

numCellsX = 100
numCellsY = 100
cellSize  = 5
color0    = (255, 255, 255)
color1    = (0, 0, 0)
colorA    = (255, 0, 0)

winWidth  = numCellsX*cellSize
winHeight = numCellsY*cellSize

# init pygame
pg.init()
screen = pg.display.set_mode( (winWidth, winHeight) )
pg.display.set_caption('Langton ant')
pg.mouse.set_visible(True)

theStage = np.zeros( (numCellsY, numCellsX), dtype=np.uint8 )

# one ant
ants = [Ant(50, 50)]

# multiple ants with different starting directions
# ants = [Ant(50, 50), Ant(40,23), Ant(10, 43, 1), Ant(60, 20, 2), Ant(74, 83, 0)] 

# one Ant and one InvertedAnt
# ants = [Ant(25, 50), InvertedAnt(75, 50)]


while 1:

    # process pygame events
    for event in pg.event.get():

        # exit app
        if event.type == pg.QUIT: 
            sys.exit()

        # add new ant on mouse click
        if event.type == pg.MOUSEBUTTONUP: 
            pos = pg.mouse.get_pos()
            ants.append(Ant((int)(pos[0]/cellSize), (int)(pos[1]/cellSize)))

    drawStage(theStage)
    
    for ant in ants:
        ant.update(theStage)
        ant.move(theStage)
        ant.draw()
    
    pg.display.flip()

