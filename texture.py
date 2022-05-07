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
