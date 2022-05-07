import imgui
from texture import Texture


class Window(object):
    def __init__(self):
        super(Window, self).__init__()

    @property
    def window_name(self):
        return "Window"

    def render(self):
        pass

    def update(self):
        pass


class TestTextureWindow(Window):
    def __init__(self):
        super(TestTextureWindow, self).__init__()
        self.texture = Texture("youtube-music7134.jpg")

    def render(self):
        imgui.begin("Test Texture")

        imgui.image(self.texture.texture_id, self.texture.width, self.texture.height)

        imgui.end()
