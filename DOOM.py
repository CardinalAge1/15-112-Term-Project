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
import Things


class MyApp(ShowBase):

    def __init__(self):
        self.fall = 0

        ShowBase.__init__(self)
        self.height = base.camera.getZ()
        # Load the environment model.

        # Reparent the model to render.
        # Apply scale and position transforms on the model.
        base.disableMouse()
        self.createKeyControls()

        mySound = base.loader.loadSfx(
            """/Users/danielgarcia/Docs/15-112-Term-Project/models/At Doom's Gate.ogg""")
        mySound.play()

        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0,
                       "turn-left": 0, "turn-right": 0, "fast": 0, "jump": 0}
        timer = 0.2
        taskMgr.doMethodLater(timer, self.move, "move")

        # Initialize the collision traverser.
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True)

        # Initialize the Pusher collision handler.
        pusher = CollisionHandlerPusher()

        # Create a collision node for this object.
        cNode = CollisionNode('camera')
        # Attach a collision sphere solid to the collision node.
        cNode.addSolid(CollisionSphere(2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(-2, 0, 0, .75))
        cNode.addSolid(CollisionSphere(0, 2, 0, .75))
        cNode.addSolid(CollisionSphere(0, -2, 0, .75))
        cNode.addSolid(CollisionSphere(0, 0, -10, .75))
        cNode.addSolid(CollisionSphere(0, 0, 2, .75))
        # Attach the collision node to the object's model.
        cameraC = base.camera.attachNewNode(cNode)
        # Set the object's collision node to render as visible.
        self.scene = Things.Thing(base, 0, 0, 0, 0.25,
                                  "/Users/danielgarcia/Docs/15-112-Term-Project/models/Test.egg")

        # Add the Pusher collision handler to the collision traverser.
        base.cTrav.addCollider(cameraC, pusher)
        # Add the 'camera' collision node to the Pusher collision handler.
        pusher.addCollider(cameraC, base.camera, base.drive.node())

    def setKey(self, key, value):
        self.keyMap[key] = value

    def createKeyControls(self):

        # directional movement
        self.accept("w", self.setKey, ["left", 1])
        self.accept("s", self.setKey, ["right", 1])
        self.accept("a", self.setKey, ["backward", 1])
        self.accept("d", self.setKey, ["forward", 1])
        self.accept("shift-w", self.setKey, ["left", 1])
        self.accept("shift-s", self.setKey, ["right", 1])
        self.accept("shift-a", self.setKey, ["backward", 1])
        self.accept("shift-d", self.setKey, ["forward", 1])
        self.accept("shift", self.setKey, ["fast", 1])
        self.accept("space-up", self.setKey, ["jump", 1])

        # directional movement - arrow up
        self.accept("shift-w-up", self.setKey, ["left", 0])
        self.accept("shift-s-up", self.setKey, ["right", 0])
        self.accept("shift-a-up", self.setKey, ["backward", 0])
        self.accept("shift-d-up", self.setKey, ["forward", 0])
        self.accept("w-up", self.setKey, ["left", 0])
        self.accept("s-up", self.setKey, ["right", 0])
        self.accept("a-up", self.setKey, ["backward", 0])
        self.accept("d-up", self.setKey, ["forward", 0])
        self.accept("shift-up", self.setKey, ["fast", 0])

        # turning movement
        self.accept("shift-arrow_left", self.setKey, ["turn-left", 1])
        self.accept("shift-arrow_right", self.setKey, ["turn-right", 1])
        self.accept("shift-arrow_left-up", self.setKey, ["turn-left", 0])
        self.accept("shift-arrow_right-up", self.setKey, ["turn-right", 0])
        self.accept("arrow_left", self.setKey, ["turn-left", 1])
        self.accept("arrow_right", self.setKey, ["turn-right", 1])
        self.accept("arrow_left-up", self.setKey, ["turn-left", 0])
        self.accept("arrow_right-up", self.setKey, ["turn-right", 0])

    def move(self, task):
        (x, y, z) = base.camera.getPos()
        (h, p, r) = base.camera.getHpr()

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

        base.camera.setFluidPos(base.camera, dx, dy, dz)
        if newZ == self.height:
            self.fall = 0
        else:
            self.height = newZ

        base.camera.setH(newH)
        base.camera.setP(newP)
        base.camera.setR(newR)

        return task.cont


app = MyApp()
app.run()
# Test"""
