import hashlib
import os
import platform
from io import BytesIO

from PIL import Image

from glfw_window import surface_to_texture_id_glfw, save_image_to_cache_glfw
from sdl2_window import surface_to_texture_id_sdl2, save_image_to_cache_sdl2

is_x86 = platform.machine() in ("i386", "AMD64", "x86_64")


def surface_to_texture_id(path):
    if is_x86:
        return surface_to_texture_id_sdl2(path)
    else:
        return surface_to_texture_id_glfw(path)


def image_exist(url):
    # find image use by os.path.exists.
    url_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
    image_name = url_md5 + ".png"
    image_path = "res/cache/" + image_name
    return os.path.exists(image_path)


def save_image_to_cache(url, contents):
    if is_x86:
        return save_image_to_cache_sdl2(url, contents)
    else:
        return save_image_to_cache_glfw(url, contents)

