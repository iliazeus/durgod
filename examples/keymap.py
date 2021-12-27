from durgod import Keyboard, Matrix, Key


def main():
    kb = Keyboard.find()

    if kb is None:
        raise ValueError('keyboard not found')

    keymap = kb.get_default_keymap()

    keymap.keys[Matrix.SCROLLLOCK] = Key.MOD_LSHIFT | Key.Z

    kb.apply_keymap(keymap)


if __name__ == '__main__':
    main()
