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


class Muzak(object):
    def __init__(self, base):
        self.base = base
        mySound = self.base.loader.loadSfx(
            """/Users/danielgarcia/Docs/15-112-Term-Project/models/At Doom's Gate.ogg""")
        mySound.play()
