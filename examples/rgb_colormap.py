from durgod import Keyboard, Matrix
import time


def main():
    kb = Keyboard.find()

    if kb is None:
        raise ValueError('keyboard not found')

    keys = [Matrix.D, Matrix.U, Matrix.R, Matrix.G, Matrix.O, Matrix.D]

    kb.disable_rgb()

    for key in keys:
        colormap = kb.get_default_colormap()

        colormap.colors[key] = 0xff0000

        kb.apply_colormap(colormap)

        time.sleep(0.5)

    kb.disable_rgb()


if __name__ == '__main__':
    main()
