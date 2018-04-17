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


class Thing(ShowBase):
    def __init__(self, base, x, y, z, scale, modelPath):
        self.x = x
        self.y = y
        self.z = z
        self.model = base.loader.loadModel(modelPath)
        self.model.reparentTo(render)
        self.model.setScale(scale, scale, scale)
        self.model.setFluidPos(self.x, self.y, self.z)
