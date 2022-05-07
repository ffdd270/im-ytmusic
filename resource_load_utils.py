import hashlib
from io import BytesIO
from PIL import Image


def get_image_path(url):
    url_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
    image_name = url_md5 + ".png"
    return image_name


def save_image_to_cache_from_bytes(url, contents):
    # Image open contents.
    image = Image.open(BytesIO(contents))
    # url to md5.
    image_name = get_image_path(url)
    image_path = "cache/" + image_name
    image.save("res/" + image_path, "PNG")
    return image_name
