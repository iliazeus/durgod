from durgod import Keyboard, Colormap
from PIL import Image

from math import trunc
from sys import argv
from time import sleep


def main():
    filename = argv[1]
    out_filename = argv[2]

    if filename is None:
        print('filename argument missing')
        exit(1)

    kb = Keyboard.find()

    if kb is None:
        raise ValueError('keyboard not found')

    image = Image.open(filename)
    out_image = image.copy()

    layout = kb.get_layout()
    colormap = Colormap([])

    for (x, y) in layout.get_centers():
        pixel_x = trunc(x * image.width / layout.width)
        pixel_y = trunc(y * image.height / layout.height)

        if pixel_x >= image.width: pixel_x = image.width - 1
        if pixel_y >= image.height: pixel_y = image.height - 1

        out_image.putpixel((pixel_x, pixel_y), (255, 0, 0, 255))

        pixel = image.getpixel((pixel_x, pixel_y))
        color: int = pixel[0] << 16 | pixel[1] << 8 | pixel[2]

        colormap.colors.append(color)

    if out_filename is not None:
        out_image.save(out_filename)

    kb.disable_rgb()
    kb.apply_colormap(colormap)

    sleep(5)

    kb.disable_rgb()


if __name__ == '__main__':
    main()
