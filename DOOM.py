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

        ShowBase.__init__(self)
        # Load the environment model.

        # Reparent the model to render.
        # Apply scale and position transforms on the model.
        base.disableMouse()

        mySound = base.loader.loadSfx(
            """/Users/danielgarcia/Docs/15-112-Term-Project/models/At Doom's Gate.ogg""")
        mySound.play()

        # Initialize the Pusher collision handler.
        pusher = CollisionHandlerPusher()
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True)

        timer = 0.2
        self.doomGuy = Things.Doomguy(base, (0, 0, 0), (0, 0, 0),
                                      base.camera, pusher, base.cTrav)

        self.createKeyControls()
        taskMgr.doMethodLater(timer, self.doomGuy.move, "move")

        self.scene = Things.Thing(base, 0, 0, 0, 0.25,
                                  "/Users/danielgarcia/Docs/15-112-Term-Project/models/Test.egg")

    def createKeyControls(self):

        # directional movement
        self.accept("w", self.doomGuy.setKey, ["left", 1])
        self.accept("s", self.doomGuy.setKey, ["right", 1])
        self.accept("a", self.doomGuy.setKey, ["backward", 1])
        self.accept("d", self.doomGuy.setKey, ["forward", 1])
        self.accept("shift-w", self.doomGuy.setKey, ["left", 1])
        self.accept("shift-s", self.doomGuy.setKey, ["right", 1])
        self.accept("shift-a", self.doomGuy.setKey, ["backward", 1])
        self.accept("shift-d", self.doomGuy.setKey, ["forward", 1])
        self.accept("shift", self.doomGuy.setKey, ["fast", 1])
        self.accept("space-up", self.doomGuy.setKey, ["jump", 1])

        # directional movement - arrow up
        self.accept("shift-w-up", self.doomGuy.setKey, ["left", 0])
        self.accept("shift-s-up", self.doomGuy.setKey, ["right", 0])
        self.accept("shift-a-up", self.doomGuy.setKey, ["backward", 0])
        self.accept("shift-d-up", self.doomGuy.setKey, ["forward", 0])
        self.accept("w-up", self.doomGuy.setKey, ["left", 0])
        self.accept("s-up", self.doomGuy.setKey, ["right", 0])
        self.accept("a-up", self.doomGuy.setKey, ["backward", 0])
        self.accept("d-up", self.doomGuy.setKey, ["forward", 0])
        self.accept("shift-up", self.doomGuy.setKey, ["fast", 0])

        # turning movement
        self.accept("shift-arrow_left", self.doomGuy.setKey, ["turn-left", 1])
        self.accept("shift-arrow_right", self.doomGuy.setKey, ["turn-right", 1])
        self.accept("shift-arrow_left-up",
                    self.doomGuy.setKey, ["turn-left", 0])
        self.accept("shift-arrow_right-up",
                    self.doomGuy.setKey, ["turn-right", 0])
        self.accept("arrow_left", self.doomGuy.setKey, ["turn-left", 1])
        self.accept("arrow_right", self.doomGuy.setKey, ["turn-right", 1])
        self.accept("arrow_left-up", self.doomGuy.setKey, ["turn-left", 0])
        self.accept("arrow_right-up", self.doomGuy.setKey, ["turn-right", 0])


app = MyApp()
app.run()
# Test"""
