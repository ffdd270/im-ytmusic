from ytmusicapi import YTMusic
import threading


class YTMusicAPI(object):
    def __init__(self):
        super(YTMusicAPI, self).__init__()
        self.api_key = ""
        self.ytmusic = YTMusic("headers_auth.json")

    def _async_get_home(self, callback):
        home = self.ytmusic.get_home()
        callback(home)

    def async_get_home(self, callback):
        thread = threading.Thread(target=self._async_get_home,
                                  args=(callback,))

        thread.start()

    def get_home(self):
        return self.ytmusic.get_home()
