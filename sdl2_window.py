# -*- coding: utf-8 -*-

from sdl2 import *
import sdl2.ext
import sys
import ctypes
import OpenGL.GL as gl
from imgui.integrations.sdl2 import SDL2Renderer
import imgui
from typing import Optional

RES: Optional[sdl2.ext.Resources] = None
SDL2_EVENT: Optional[sdl2.SDL_Event] = None
SDL2_WINDOW: Optional[sdl2.SDL_Window] = None
SDL2_RENDERER: Optional[sdl2.SDL_Renderer] = None
SDL2_IMGUI_RENDERER: Optional[SDL2Renderer] = None
GL_CONTEXT: Optional[SDL_GLContext] = None
RUNNING = True


def init_window_sdl2():
    global SDL2_EVENT, SDL2_WINDOW, SDL2_RENDERER, SDL2_IMGUI_RENDERER, GL_CONTEXT, RES
    SDL2_WINDOW, SDL2_RENDERER, GL_CONTEXT = impl_pysdl2_init()
    imgui.create_context()
    SDL2_IMGUI_RENDERER = SDL2Renderer(SDL2_WINDOW)
    SDL2_EVENT = SDL_Event()
    RES = sdl2.ext.Resources(__file__, "res")


def is_running_sdl2():
    return RUNNING


def poll_event_sdl2():
    global SDL2_EVENT, RUNNING
    while SDL_PollEvent(ctypes.byref(SDL2_EVENT)) != 0:
        if SDL2_EVENT.type == SDL_QUIT:
            RUNNING = False
            break
        SDL2_IMGUI_RENDERER.process_event(SDL2_EVENT)


def pre_imgui_new_frame_sdl2():
    SDL2_IMGUI_RENDERER.process_inputs()


def after_imgui_new_frame_sdl2():
    gl.glClearColor(1., 1., 1., 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)


def after_imgui_redner_sdl2():
    SDL2_IMGUI_RENDERER.render(imgui.get_draw_data())
    SDL_GL_SwapWindow(SDL2_WINDOW)


def shutdown_sdl2():
    SDL2_IMGUI_RENDERER.shutdown()
    SDL_GL_DeleteContext(GL_CONTEXT)
    SDL_DestroyWindow(SDL_Window)
    SDL_Quit()


def surface_to_texture_id_sdl2(path):
    global RES

    image = sdl2.ext.load_image(RES.get_path(path))
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    gl_format = gl.GL_RGBA
    if image.format.contents.BytesPerPixel == 4:
        if image.format.contents.Rmask == 0x000000ff:
            gl_format = gl.GL_RGBA
        else:
            gl_format = gl.GL_BRGA
    elif image.format.contents.BytesPerPixel == 3:
        if image.format.contents.Rmask == 0x000000ff:
            gl_format = gl.GL_RGB
        else:
            gl_format = gl.GL_BGR

    if SDL_MUSTLOCK(image):
        SDL_LockSurface(image)

    array = ctypes.cast(image.pixels, ctypes.POINTER(ctypes.c_uint8))
    width = image.w
    height = image.h
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl_format,
                    gl.GL_UNSIGNED_BYTE, array)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    # release the surface
    if SDL_MUSTLOCK(image):
        SDL_UnlockSurface(image)

    SDL_FreeSurface(image)
    return texture_id, width, height


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
