# -*- coding: utf-8 -*-
from sdl2 import *
import sdl2.ext
import sys
import ctypes
import OpenGL.GL as gl

import imgui
from imgui.integrations.sdl2 import SDL2Renderer

from main_menu import main_menu

RES = None


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


def draw_windows(texture):
    main_menu()

    imgui.show_test_window()

    imgui.begin("Custom window", True)
    imgui.text("Bar")
    imgui.image(texture.texture_id, texture.width, texture.height)
    imgui.text_colored("Eggs", 0.2, 1., 0.)
    imgui.end()


def surface_to_texture_id(path):
    global RES

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


def main():
    window, renderer, gl_context = impl_pysdl2_init()
    imgui.create_context()
    impl = SDL2Renderer(window)

    running = True
    event = SDL_Event()
    # set global RES
    global RES
    RES = sdl2.ext.Resources(__file__, "res")
    texture = Texture("youtube-music7134.jpg")

    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break
            impl.process_event(event)
        impl.process_inputs()
        imgui.new_frame()

        draw_windows(texture)

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        SDL_GL_SwapWindow(window)

    impl.shutdown()
    SDL_GL_DeleteContext(gl_context)
    SDL_DestroyWindow(window)
    SDL_Quit()


def impl_pysdl2_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/SDL2 example"

    if SDL_Init(SDL_INIT_EVERYTHING) < 0:
        print("Error: SDL could not initialize! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 16)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)

    SDL_SetHint(SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
    SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    window = SDL_CreateWindow(window_name.encode('utf-8'),
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              width, height,
                              SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)

    if window is None:
        print("Error: Window could not be created! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    gl_context = SDL_GL_CreateContext(window)
    if gl_context is None:
        print("Error: Cannot create OpenGL Context! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    if renderer is None:
        print("Error: Cannot create OpenGL Context! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    SDL_GL_MakeCurrent(window, gl_context)
    if SDL_GL_SetSwapInterval(1) < 0:
        print("Warning: Unable to set VSync! SDL Error: " + SDL_GetError().decode("utf-8"))
        exit(1)

    return window, renderer, gl_context


if __name__ == "__main__":
    main()
