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
from Muzak import *
import Bullet


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        # Load the environment model.

        # Reparent the model to render.
        # Apply scale and position transforms on the model.
        base.disableMouse()
        """audio = Muzak(base)"""
        self.mouseX = 0
        self.mouseY = 0
        if base.mouseWatcherNode.hasMouse():
            self.mouseX = base.mouseWatcherNode.getMouseX()
            self.mouseY = base.mouseWatcherNode.getMouseY()

        # Initialize the Pusher collision handler.
        pusher = CollisionHandlerPusher()
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True)

        timer = 0.2
        self.doomGuy = Things.Doomguy(base, (0, 1, 0), (0, 0, 0),
                                      base.camera, pusher, base.cTrav)

        self.createKeyControls()
        taskMgr.doMethodLater(timer, self.doomGuy.move, "move")
        taskMgr.doMethodLater(timer, Bullet.step, "step")
        taskMgr.doMethodLater(0.1, self.doomGuy.shoot, "shoot")
        taskMgr.doMethodLater(timer, self.doomGuy.checkHit, "checkHit")

        self.scene = Things.Thing(base, 0, 0, 0, 0.25,
                                  "/Users/danielgarcia/Docs/15-112-Term-Project/models/Test.egg")

    def createKeyControls(self):

        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)

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
        self.accept("mouse1", self.doomGuy.setKey, ["shoot", 1])
        self.accept("shift-mouse1", self.doomGuy.setKey, ["shoot", 1])
        self.accept("mouse1-up", self.doomGuy.setKey, ["shoot", 0])
        self.accept("shift-mouse1-up", self.doomGuy.setKey, ["shoot", 0])
        self.accept("wheel_up", self.doomGuy.switchWeapon, ["up"])
        self.accept("wheel_down", self.doomGuy.switchWeapon, ["down"])
        self.accept("shift-wheel_up", self.doomGuy.switchWeapon, ["up"])
        self.accept("shift-wheel_down", self.doomGuy.switchWeapon, ["down"])

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


app = MyApp()
app.run()
# Test"""
