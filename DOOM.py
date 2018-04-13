from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys
import math
import os
import random
from direct.task.Task import Task
import time


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # Load the environment model.
        self.scene = self.loader.loadModel(
            "/Users/danielgarcia/Docs/15-112-Term-Project/Test.egg")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-10, -10, -10)
        base.disableMouse()
        self.createKeyControls()

        mySound = base.loader.loadSfx(
            "/Users/danielgarcia/Docs/15-112-Term-Project/At Doom's Gate.ogg")
        # mySound.play()

        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0,
                       "turn-left": 0, "turn-right": 0, "fast": 0}
        timer = 0.2
        taskMgr.doMethodLater(timer, self.move, "move")

    def setKey(self, key, value):
        self.keyMap[key] = value

    def createKeyControls(self):

        # directional movement
        self.accept("w", self.setKey, ["left", 1])
        self.accept("s", self.setKey, ["right", 1])
        self.accept("a", self.setKey, ["backward", 1])
        self.accept("d", self.setKey, ["forward", 1])
        self.accept("shift", self.setKey, ["fast", 1])

        # directional movement - arrow up
        self.accept("w-up", self.setKey, ["left", 0])
        self.accept("s-up", self.setKey, ["right", 0])
        self.accept("a-up", self.setKey, ["backward", 0])
        self.accept("d-up", self.setKey, ["forward", 0])
        self.accept("shift-up", self.setKey, ["fast", 0])

        # turning movement
        self.accept("arrow_left", self.setKey, ["turn-left", 1])
        self.accept("arrow_right", self.setKey, ["turn-right", 1])
        self.accept("arrow_left-up", self.setKey, ["turn-left", 0])
        self.accept("arrow_right-up", self.setKey, ["turn-right", 0])

    def move(self, task):
        (x, y, z) = base.camera.getPos()
        (h, p, r) = base.camera.getHpr()

        (dx, dy, dz) = (0, 0, 0)
        (dh, dp, dr) = (0, 0, 0)

        if self.keyMap["forward"] > 0:
            (dx) = (1)

        elif self.keyMap["backward"] > 0:
            (dx) = (-1)

        if self.keyMap["left"] > 0:
            (dy) = (1)

        elif self.keyMap["right"] > 0:
            (dy) = (-1)

        if self.keyMap["turn-left"] > 0:
            (dh, dp, dr) = (1, 0, 0)

        elif self.keyMap["turn-right"] > 0:
            (dh, dp, dr) = (-1, 0, 0)

        (newX, newY, newZ) = x + dx, y + dy, z + dz
        (newH, newP, newR) = h + dh, p + dp, r + dr

        # update the positions & rotation
        # base.camera.setX(newX)
        # base.camera.setY(newY)
        # base.camera.setZ(newZ)
        if self.keyMap["fast"] > 0:
            base.camera.setPos(base.camera, 2 * dx, 2 * dy, 2 * dz)
        else:
            base.camera.setPos(base.camera, dx, dy, dz)

        base.camera.setH(newH)
        base.camera.setP(newP)
        base.camera.setR(newR)

        return task.cont


app = MyApp()
app.run()
# Test"""
