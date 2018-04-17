from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere
from panda3d.core import Point3
import sys
import math
import os
import random
from direct.task.Task import Task
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
import time
from panda3d.core import NodePath
from panda3d.physics import *
from direct.gui.DirectGui import DirectFrame, DirectLabel


class Doomguy(object):
    def __init__(self, base, xyz, hpr, node, pusher, traverser):
        self.x, self.y, self.z = xyz[0], xyz[1], xyz[2]
        self.h, self.p, self.r = hpr[0], hpr[1], hpr[2]
        self.node = node
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0,
                       "turn-left": 0, "turn-right": 0, "fast": 0, "jump": 0}
        self.fall = 0
        self.health = 100
        # Create a collision node for this object.
        cNode = CollisionNode('doomGuy')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(-2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(0, 2, 0, .75))
        cNode.addSolid(CollisionSphere(0, -2, 0, .75))
        cNode.addSolid(CollisionSphere(0, 0, -10, .75))
        cNode.addSolid(CollisionSphere(0, 0, 2, .75))
        # Attach the collision node to the object's model.
        doomGuyC = self.node.attachNewNode(cNode)
        # Add the Pusher collision handler to the collision traverser.
        traverser.addCollider(doomGuyC, pusher)
        # Add the 'camera' collision node to the Pusher collision handler.
        pusher.addCollider(doomGuyC, self.node, base.drive.node())

    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        (x, y, z) = self.node.getPos()
        (h, p, r) = self.node.getHpr()

        (dx, dy, dz) = (0, 0, 0)
        (dh, dp, dr) = (0, 0, 0)

        dx = self.keyMap["forward"] - self.keyMap["backward"]

        dy = self.keyMap["left"] - self.keyMap["right"]

        if self.keyMap["jump"] > 0:
            self.fall = 5
            self.keyMap["jump"] = 0

        if self.keyMap["turn-left"] > 0:
            (dh, dp, dr) = (1, 0, 0)

        elif self.keyMap["turn-right"] > 0:
            (dh, dp, dr) = (-1, 0, 0)

        if self.keyMap["fast"] > 0:
            dx *= 2
            dy *= 2

        if self.fall >= -5:
            self.fall -= 0.5
        dz += self.fall

        (newX, newY, newZ) = x + dx, y + dy, z + dz
        (newH, newP, newR) = h + dh, p + dp, r + dr

        self.node.setFluidPos(self.node, dx, dy, dz)
        if newZ == z:
            self.fall = 0
        else:
            self.height = newZ

        self.node.setH(newH)
        self.node.setP(newP)
        self.node.setR(newR)

        return task.cont


class Thing(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath):
        self.x = x
        self.y = y
        self.z = z
        self.model = base.loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)
