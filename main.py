# -*- coding: utf-8 -*-
import platform
import imgui

from imgui_window import TestTextureWindow
from yt_music_playlist import YTMusicPlaylistWindow

is_x86 = platform.machine() in ("i386", "AMD64", "x86_64")

print("is_x86?", is_x86)
if is_x86:
    from sdl2_window import init_window_sdl2, is_running_sdl2, poll_event_sdl2, pre_imgui_new_frame_sdl2, \
        after_imgui_new_frame_sdl2, after_imgui_redner_sdl2, shutdown_sdl2
else:
    from glfw_window import init_window_glfw, is_running_glfw, poll_event_glfw, pre_imgui_new_frame_glfw, \
    after_imgui_new_frame_glfw, after_imgui_render_glfw, shutdown_glfw, surface_to_texture_id_glfw


def init_window():
    if is_x86:
        init_window_sdl2()
    else:
        init_window_glfw()


def is_running():
    if is_x86:
        return is_running_sdl2()
    else:
        return is_running_glfw()


def poll_event():
    if is_x86:
        poll_event_sdl2()
    else:
        poll_event_glfw()


def pre_imgui_new_frame():
    if is_x86:
        pre_imgui_new_frame_sdl2()
    else:
        pre_imgui_new_frame_glfw()


def after_imgui_new_frame():
    if is_x86:
        after_imgui_new_frame_sdl2()
    else:
        after_imgui_new_frame_glfw()


def after_imgui_render():
    if is_x86:
        after_imgui_redner_sdl2()
    else:
        after_imgui_render_glfw()


def shutdown():
    if is_x86:
        shutdown_sdl2()
    else:
        shutdown_glfw()


windows = []


def draw_imgui_windows():

    imgui.show_test_window()
    windows[0].render()


def main():
    init_window()
    # surface_to_texture_id_glfw("res/youtube-music7134.jpg")
    windows.append(YTMusicPlaylistWindow())

    while is_running():
        poll_event()
        pre_imgui_new_frame()

        imgui.new_frame()
        draw_imgui_windows()

        after_imgui_new_frame()

        imgui.render()

        after_imgui_render()

    shutdown()


if __name__ == "__main__":
    main()
