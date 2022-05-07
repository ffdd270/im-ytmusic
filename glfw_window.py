# -*- coding: utf-8 -*-

import ctypes
import glfw
import OpenGL.GL as gl
import imgui

from imgui.integrations.glfw import GlfwRenderer
from typing import Optional

GLFW_WINDOW: Optional[ctypes.POINTER(glfw._GLFWwindow)] = None
GLFW_IMGUI_RENDERER: Optional[GlfwRenderer] = None


def init_window_glfw():
    global GLFW_WINDOW, GLFW_IMGUI_RENDERER

    imgui.create_context()
    GLFW_WINDOW = impl_glfw_init()
    GLFW_IMGUI_RENDERER = GlfwRenderer(GLFW_WINDOW)


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
    pass


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
