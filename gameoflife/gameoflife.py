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
 

Implementation of Conway's game of life
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

required modules:
    pygame   https://pypi.org/project/pygame/
    numpy    https://pypi.org/project/numpy/
 
"""

import sys
import pygame as pg
import numpy as np
import random
from time import sleep


def initStates( statesArray ):
  
    for j in range(0, statesArray.shape[0]):
        for i in range(0, statesArray.shape[1]):
            statesArray[j][i] = random.choice([0, 0, 0, 0, 1])
    
    return


def initStatesBlinker( statesArray ):
  
    statesArray[50][50] = 1
    statesArray[50][51] = 1
    statesArray[50][52] = 1
    
    return


def drawStates( statesArray ):
    
    screen.fill(color0)
    
    for j in range(0, statesArray.shape[0]):
        for i in range(0, statesArray.shape[1]):
            if statesArray[j][i] == 1:
                pg.draw.rect(screen, color1, (i*cellSize, j*cellSize, cellSize, cellSize))
    return   


def updateStates( statesArray, statesBufferArray ):
    for j in range(0, statesArray.shape[0]):
        for i in range(0, statesArray.shape[1]):
            
            n = countNeighbors(statesArray, i, j)
            
            if statesArray[j][i] == 0:
                if n == 3:
                    statesBufferArray[j][i] = 1
                else:
                    statesBufferArray[j][i] = 0
            else:
                if n <= 1:
                    statesBufferArray[j][i] = 0
                elif n <= 3:
                    statesBufferArray[j][i] = 1
                else:
                    statesBufferArray[j][i] = 0
                  
    return   


def updateStatesFast( statesArray, statesBufferArray, neighborsArray ):
    
    countNeighborsFast(statesArray, neighborsArray)
    
    for j in range(0, statesArray.shape[0]):
        for i in range(0, statesArray.shape[1]):
            
            n = neighborsArray[j][i]
            
            if statesArray[j][i] == 0:
                if n == 3:
                    statesBufferArray[j][i] = 1
                else:
                    statesBufferArray[j][i] = 0
            else:
                if n <= 1:
                    statesBufferArray[j][i] = 0
                elif n <= 3:
                    statesBufferArray[j][i] = 1
                else:
                    statesBufferArray[j][i] = 0
                  
    return   


def countNeighbors( statesArray, x, y ):
    
    xmin = max(0, x-1)
    xmax = min(x+1, statesArray.shape[1]-1)
    ymin = max(0, y-1)
    ymax = min(y+1, statesArray.shape[0]-1)
    
    cnt = 0
    
    for j in range(ymin, ymax+1):
        for i in range(xmin, xmax+1):
            if not (j == y and i == x):
                cnt += statesArray[j][i]
                
    return cnt


def countNeighborsFast( statesArray, neighborsArray ):
    neighborsArray.fill(0)
    
    neighborsArray[0:numCellsY-1, 0:numCellsX-1] += statesArray[1:numCellsY, 1:numCellsX]
    neighborsArray[0:numCellsY-1, 0:numCellsX] += statesArray[1:numCellsY, 0:numCellsX]
    neighborsArray[0:numCellsY-1, 1:numCellsX] += statesArray[1:numCellsY, 0:numCellsX-1]
    
    neighborsArray[0:numCellsY, 0:numCellsX-1] += statesArray[0:numCellsY, 1:numCellsX]
    neighborsArray[0:numCellsY, 1:numCellsX] += statesArray[0:numCellsY, 0:numCellsX-1]
    
    neighborsArray[1:numCellsY, 0:numCellsX-1] += statesArray[0:numCellsY-1, 1:numCellsX]
    neighborsArray[1:numCellsY, 0:numCellsX] += statesArray[0:numCellsY-1, 0:numCellsX]
    neighborsArray[1:numCellsY, 1:numCellsX] += statesArray[0:numCellsY-1, 0:numCellsX-1]

    return
       


numCellsX = 100
numCellsY = 100
cellSize  = 5
color0    = (255, 255, 255)
color1    = (0, 0, 0)

winWidth  = numCellsX*cellSize
winHeight = numCellsY*cellSize

# init pygame
pg.init()
screen = pg.display.set_mode( (winWidth, winHeight) )
pg.display.set_caption('Conway\'s game of life')
pg.mouse.set_visible(True)

states       = np.zeros( (numCellsY, numCellsX), dtype=np.uint8 )
statesBuffer = np.zeros( (numCellsY, numCellsX), dtype=np.uint8 )
neighbors    = np.zeros((numCellsY, numCellsX), dtype=np.uint8 )

initStates(states)

mousePressed = False

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:   # add new ant on mouse click
            mousePressed = True
        if event.type == pg.MOUSEBUTTONUP:
            mousePressed = False

    if mousePressed:
        pos = pg.mouse.get_pos()
        if states[(int)(pos[1]/cellSize), (int)(pos[0]/cellSize)] == 0:
            states[(int)(pos[1]/cellSize), (int)(pos[0]/cellSize)] = 1
        
       # sleep(0.1)

        drawStates(states)
    else:

        drawStates(states)
        
        #sleep(0.1)
        
        # updateStates(states, statesBuffer)
        updateStatesFast(states, statesBuffer, neighbors)
        
        tmp = states
        states = statesBuffer
        statesBuffer = tmp
        
    pg.display.flip()

