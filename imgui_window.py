import os

from sdl2 import *
import sdl2.ext
import sys
import ctypes
import OpenGL.GL as gl
import imgui

from PIL import Image
from io import BytesIO
import hashlib

RES = None


def init_res():
    global RES
    RES = sdl2.ext.Resources(__file__, "res")


def get_image_path(url):
    url_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
    image_name = url_md5 + ".png"
    return image_name


def save_image_to_cache(url, contents):
    # Image open contents.
    image = Image.open(BytesIO(contents))
    # url to md5.
    image_name = get_image_path(url)
    image_path = "cache/" + image_name
    image.save("res/" + image_path, "PNG")
    RES.scan("res")
    return image_name


def image_exist(url):
    # find image use by os.path.exists.
    url_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
    image_name = url_md5 + ".png"
    image_path = "res/cache/" + image_name
    return os.path.exists(image_path)


def surface_to_texture_id(path):
    image = sdl2.ext.load_image(RES.get_path(path))
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    format = gl.GL_RGBA
    if image.format.contents.BytesPerPixel == 4:
        if image.format.contents.Rmask == 0x000000ff:
            format = gl.GL_RGBA
        else:
            format = gl.GL_BRGA
    elif image.format.contents.BytesPerPixel == 3:
        if image.format.contents.Rmask == 0x000000ff:
            format = gl.GL_RGB
        else:
            format = gl.GL_BGR

    if SDL_MUSTLOCK(image):
        SDL_LockSurface(image)

    array = ctypes.cast(image.pixels, ctypes.POINTER(ctypes.c_uint8))
    width = image.w
    height = image.h
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, format,
                    gl.GL_UNSIGNED_BYTE, array)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    # release the surface
    if SDL_MUSTLOCK(image):
        SDL_UnlockSurface(image)

    SDL_FreeSurface(image)
    return texture_id, width, height


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


class Texture(object):
    def __init__(self, path):
        super(Texture, self).__init__()
        self.path = path
        # get texture_id, width, height by surface_to_texture_id function.
        self._texture_id, self._width, self._height = surface_to_texture_id(path)

    @property
    def texture_id(self):
        return self._texture_id

    @texture_id.setter
    def texture_id(self, value):
        self._texture_id = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
