import platform

from glfw_window import surface_to_texture_id_glfw
from sdl2_window import surface_to_texture_id_sdl2

is_x86 = platform.machine() in ("i386", "AMD64", "x86_64")


def surface_to_texture_id(path):
    if is_x86:
        return surface_to_texture_id_sdl2(path)
    else:
        return surface_to_texture_id_glfw(path)
