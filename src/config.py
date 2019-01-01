class Config(object):
    """
    Config collects global configuration variables.
    """

    fps: int = 60
    scale: int = 40

    @property
    def height(self) -> int:
        """
        Get game board pixel height.
        """
        return self.scale * 20

    @property
    def width(self) -> int:
        """
        Get game board pixel width.
        """
        return self.scale * 10
