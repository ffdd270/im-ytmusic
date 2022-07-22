import imgui

from imgui_window import Window, Texture
from resource_load_interface import save_image_to_cache, image_exist
from resource_load_utils import get_image_path
from ytmusic_api import YTMusicAPI


class YTMusicAPITestWindow(Window):
    def __init__(self):
        super().__init__()
        self.home_res = None
        self.yt = YTMusicAPI()
        self.async_begin = False

    def window_name(self):
        return "YTMusicAPITestWindow"

    def async_get_home(self):
        return self.yt.get_home()

    def set_home(self, res):
        self.home_res = res
        self.async_begin = False

    def render(self):
        imgui.begin(self.window_name())
        if imgui.button("SEND REQUEST : HOME"):
            self.yt.async_get_home(lambda res: self.set_home(res))
            self.async_begin = True

        if self.async_begin:
            imgui.text("SENDING REQUEST... PLEASE WAIT...")

        if (self.home_res is not None) and (not self.async_begin):
            imgui.text("RESPONSE :")
            imgui.push_item_width(100)
            imgui.text_wrapped(str(self.home_res))
            imgui.pop_item_width()

        imgui.end()