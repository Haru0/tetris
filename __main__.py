import os

from src.game import Game


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    game = Game()
    game.init()
    game.run()


if __name__ == '__main__':
    main()
