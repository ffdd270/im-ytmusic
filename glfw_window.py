# -*- coding: utf-8 -*-

import ctypes
import glfw
import OpenGL.GL as gl
import imgui
import os

import numpy
from PIL import Image
from imgui.integrations.glfw import GlfwRenderer
from typing import Optional

from resource_load_utils import save_image_to_cache_from_bytes

GLFW_WINDOW: Optional[ctypes.POINTER(glfw._GLFWwindow)] = None
GLFW_IMGUI_RENDERER: Optional[GlfwRenderer] = None
FILE_MAP = {}


def glfw_file_scan():
    global FILE_MAP

    FILE_MAP = {}

    for subdir, dirs, files in os.walk("res/"):
        for file in files:
            FILE_MAP[file] = subdir + "/" + file


def init_window_glfw():
    global GLFW_WINDOW, GLFW_IMGUI_RENDERER

    imgui.create_context()
    GLFW_WINDOW = impl_glfw_init()
    GLFW_IMGUI_RENDERER = GlfwRenderer(GLFW_WINDOW)
    glfw_file_scan()


def is_running_glfw():
    global GLFW_WINDOW
    return not glfw.window_should_close(GLFW_WINDOW)


def poll_event_glfw():
    glfw.poll_events()


def pre_imgui_new_frame_glfw():
    global GLFW_IMGUI_RENDERER
    GLFW_IMGUI_RENDERER.process_inputs()


def after_imgui_new_frame_glfw():
    gl.glClearColor(1., 1., 1., 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)


def after_imgui_render_glfw():
    global GLFW_WINDOW, GLFW_IMGUI_RENDERER
    GLFW_IMGUI_RENDERER.render(imgui.get_draw_data())
    glfw.swap_buffers(GLFW_WINDOW)


def shutdown_glfw():
    global GLFW_WINDOW, GLFW_IMGUI_RENDERER
    GLFW_IMGUI_RENDERER.shutdown()
    glfw.terminate()


def surface_to_texture_id_glfw(path):
    global FILE_MAP
    img = Image.open(FILE_MAP[path])
    # RGBA로 바꿔준다. 매직.
    img = img.convert("RGBA")
    width, height = img.size

    array = numpy.array(list(img.getdata()), numpy.uint8)

    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                    gl.GL_UNSIGNED_BYTE, array)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    return texture_id, width, height


def save_image_to_cache_glfw(url, contents):
    image_name = save_image_to_cache_from_bytes(url, contents)
    glfw_file_scan()
    return image_name


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window
