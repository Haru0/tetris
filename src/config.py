class Config(object):
    """
        Config collects general configuration variables such as:
         - Size of a block
         - Maximum frame rate
    """

    fps = 60
    scale = 40

    @property
    def height(self) -> int:
        return self.scale * 20

    @property
    def width(self) -> int:
        return self.scale * 10
