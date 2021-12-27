from durgod import Keyboard, RgbEffect
import time


def main():
    kb = Keyboard.find()

    if kb is None:
        raise ValueError('keyboard not found')

    # skipping RgbEffect.PLAY and RgbEffect.STOP
    effects = list(RgbEffect)[2:]

    for effect in effects:
        kb.apply_rgb_effect(effect)
        time.sleep(5)

    kb.disable_rgb()


if __name__ == '__main__':
    main()
