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
 

Tree object with drawing capability

required modules:
    pygame   https://pypi.org/project/pygame/
 
"""

import sys
import pygame as pg
from time import sleep
import math

# TreeNode class. A tree node connects to its children
class TreeNode:

    # Constructor: 
    def __init__(self, depth = 0):
        self.children = []
        self.depth = depth

    def isLeaf(self):
        return len(self.children) == 0


# Tree class. The tree is represented by a root TreeNode and has functions
# to draw the tree.
class Tree:

    # constructor. 
    # treeDepth:   specifies the depth of the tree and must be >= 1
    # numChildren: specifies the number of children of a node, must be >= 1
    def __init__(self, treeDepth, numChildren):
        self.rootNode = self.__createTree(treeDepth, numChildren)

    # creates the tree recursively and is called by the constructor. don't call from outside.
    def __createTree(self, treeDepth, numChildren):
        
        node = TreeNode(treeDepth)

        if (treeDepth > 1):
            for i in range(numChildren):
                node.children.append(self.__createTree(treeDepth-1, numChildren))
        
        return node


    def getTreeDepth(self):
        return self.rootNode.depth

    # draws the whole tree
    # pos:           (x,y)-position in the window, where to draw the root node
    # angle:         direction of tree. children will be drawn in direction of angle (in degrees). 0 is to the right, 90 down, 180 left, 270 or -90 is up.
    # angleDelta:    angle between two child branches
    # length:        length of the first top level branches
    # lengthScaling: branch length is scaled by lengthScaling for every tree level descending down the tree
    # innerColor:    color of the tree's inner branches
    # leafColor:     color of the tree's leaf branches
    # stepTime:      if > 0 each branch is drawn after a delay of stepTime seconds
    def draw(self, pos, angle, angleDelta, length, lengthScaling, innerColor, leafColor, stepTime = 0):
        self.__drawTree(self.rootNode, pos, angle, angleDelta, length, lengthScaling, innerColor, leafColor, stepTime)


    # draws a tree stored in the given TreeNode recursively. called by the draw function. 
    def __drawTree(self, node, pos, angle, angleDelta, length, lengthScaling, innerColor, leafColor, stepTime = 0):

        # get number of children
        n = len(node.children)

        # if the current node has children, compute position of the child nodes and draw branches to children
        for i in range(n):

            # compute direction of the child node (= direction of the branch)
            alpha = angle - angleDelta*(n-1)*0.5 + i*angleDelta 

            # compute child position
            # child's x = parent's x  +  branch length * cos( direction angle )
            # child's y = parent's y  +  branch length * sin( direction angle )
            childPos = ( pos[0] + length * math.cos(math.radians(alpha)), pos[1] + length * math.sin(math.radians(alpha)) )

            # draw branch 
            if node.depth <= 2:
                pg.draw.line(screen, leafColor, pos, childPos)  # leaf branch
            else:
                pg.draw.line(screen, innerColor, pos, childPos) # inner branch

            # delay next draw by stepTime seconds
            if stepTime > 0:
                pg.display.flip()
                sleep(stepTime)
            

            # draw child branches of the child node
            self.__drawTree( node.children[i], childPos, alpha, angleDelta, length*lengthScaling, lengthScaling, innerColor, leafColor, stepTime)


# colors definitions
colorBg  = (0, 0, 0)
colorInner  = (255, 255, 255)
colorLeaf = (198, 0, 0)

# window size
winWidth  = 1400
winHeight = 800

# tree drawing parameters
maxLength = 250       # branch length
maxLengthScaling = 1  # maximum scaling of branch lenghts
maxAngleDelta = 360   # maximum angles between branches of one tree node
nx = 1                # normalized mouse coordinate in x-direction
ny = 1                # normalized mouse coordinate in y-direction

# init pygame
pg.init()
screen = pg.display.set_mode( (winWidth, winHeight) )
pg.display.set_caption('Tree')
pg.mouse.set_visible(True)

# the tree object
tree = Tree(7, 2)


while 1:

    # process pygame events
    for event in pg.event.get():

        # quit application
        if event.type == pg.QUIT: 
            sys.exit()

        # normalize mouse coordinates
        if event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            nx = pos[0] / winWidth
            ny = pos[1] / winHeight
        

    # draw background
    screen.fill(colorBg)

    # draw tree with branch angles depending on mouse's x-coordinate and branch length scaling depending on mouse's y-coordinate
    tree.draw( (winWidth*0.5, winHeight*0.7), -90, maxAngleDelta*nx, 100, maxLengthScaling*ny, colorInner, colorLeaf, 0 )
    
    pg.display.flip()

