import imgui

from imgui_window import Window, save_image_to_cache, Texture, image_exist, get_image_path
from test_yt_music_data import get_test_data
import requests


class YTMusicPlayList:
    def __init__(self, playlist):
        super(YTMusicPlayList, self).__init__()
        self.content = playlist
        self.elements = []
        for content in playlist['contents']:
            self.elements.append(YTMusicPlayListElement(content))

    @property
    def title(self):
        return self.content['title']

    @property
    def elements(self):
        return self.elements


class YTMusicPlayListElement:
    def __init__(self, content):
        super(YTMusicPlayListElement, self).__init__()
        self.content = content
        thumbnail_url = self.thumbnail
        thumbnail_exist = image_exist(thumbnail_url)
        if thumbnail_exist:
            self._thumbnail_texture = Texture(get_image_path(thumbnail_url))
        else:
            image = requests.get(thumbnail_url).content
            save_image_to_cache(thumbnail_url, image)
            self._thumbnail_texture = Texture(get_image_path(thumbnail_url))

    @property
    def title(self):
        return self.content['title']

    @property
    def thumbnail(self):
        return self.content['thumbnails'][0]['url']

    @property
    def thumbnail_texture(self):
        return self._thumbnail_texture


class YTMusicPlaylistWindow(Window):
    def __init__(self):
        super().__init__()
        self.playlists_raw_data = get_test_data()
        self.playlists = []

        for playlist in self.playlists_raw_data:
            self.playlists.append(YTMusicPlayList(playlist))

    def window_name(self):
        return "YT Music Playlist"

    def render_per_playlist(self, playlist):
        imgui.begin_child("Playlist", 0, 0, True)

        imgui.text(playlist["title"])

        for element in playlist.elements:
            imgui.text(element.title)
            imgui.same_line()
            texture = element.thumbnail_texture
            imgui.image(texture.texture_id, texture.width, texture.height)

        imgui.end_child()

    def render(self):
        imgui.begin(self.window_name())
        self.render_per_playlist(self.playlists[0])
        imgui.end()
