from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos
from direct.task import Task


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
        base.useDrive()

        mySound = base.loader.loadSfx(
            "/Users/danielgarcia/Docs/15-112-Term-Project/At Doom's Gate.ogg")
        mySound.play()

        # Add the spinCameraTask procedure to the task manager.


app = MyApp()
app.run()
# Test
