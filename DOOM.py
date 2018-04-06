from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel(
            "model\environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 5)
        base.disableMouse()
        base.useDrive()


app = MyApp()
app.run()
# Test
