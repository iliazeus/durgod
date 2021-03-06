import time
import usb

from .constants import *
from .messages import *


class Keymap:
    """
    Represents a mapping for a "custom layer" of a keyboard.

    On a Durgod Taurus K320 Nebula, it is toggled by Fn+F12.
    """

    ROW_LENGTH = 8
    ROW_COUNT = 16

    def __init__(self, keys: list[Key]):
        self.keys = keys

    def get_row(self, index: int) -> list[Key]:
        assert 0 <= index < Keymap.ROW_COUNT

        start = index * Keymap.ROW_LENGTH
        end = (index + 1) * Keymap.ROW_LENGTH

        return self.keys[start:end]


class Colormap:
    """
    Represents a mapping for the per-key RGB backlight.
    """

    ROW_LENGTH = 14
    ROW_COUNT = 9

    def __init__(self, colors: list[int]):
        self.colors = colors

    def get_row(self, index: int) -> list[int]:
        assert 0 <= index < Colormap.ROW_COUNT

        start = index * Colormap.ROW_LENGTH
        end = (index + 1) * Colormap.ROW_LENGTH

        return self.colors[start:end]


class Layout:
    """
    Represents the physical keyboard layout.

    The format is inspired by https://keyboard-layout-editor.com,
    but not exactly the same.
    """

    class Group:
        def __init__(
            self,
            count: int = 0,
            skip: int = 0,
            row: bool = False,
            x: float = 0,
            y: float = 0,
            w: float = 1,
            h: float = 1,
        ):
            self.count = count
            self.skip = skip
            self.row = row
            self.x = x
            self.y = y
            self.w = w
            self.h = h

    def __init__(self, width: float, height: float, groups: list[Group]):
        self.width = width
        self.height = height
        self.groups = groups

    def get_centers(self) -> list[tuple[float, float]]:
        points: list[tuple[float, float]] = []

        x: float = 0
        y: float = 0

        for group in self.groups:
            if group.row:
                x = 0
                y += 1

            x += group.x
            y += group.y

            for i in range(group.skip):
                points.append((0, 0))

            for i in range(group.count):
                points.append((x + group.w/2, y + group.h/2))
                x += group.w

        return points


class Keyboard:
    """Represents a Durgod Taurus keyboard."""

    def find(
        product_id: KeyboardId = None,
        vendor_id: VendorId = VendorId.HOKSI_TECHNOLOGY,
    ) -> 'Keyboard':
        # a small timeout to wait until all keys are released
        time.sleep(0.2)

        device = None

        if product_id is not None:
            device = usb.core.find(
                idVendor=vendor_id,
                idProduct=product_id,
            )
        else:
            device = usb.core.find(
                idVendor=vendor_id,
            )

        if device is None:
            return None

        return Keyboard(device)

    def __init__(self, device: usb.Device):
        self.device = device

        config = device.get_active_configuration()

        interface = usb.util.find_descriptor(config, bInterfaceSubClass=0x00)
        if self.device.is_kernel_driver_active(interface.index):
            self.device.detach_kernel_driver(interface.index)

    def _write(self, msg: Message, pad_to_length: int = 64):
        msg_bytes = msg.pack()
        msg_bytes += bytes(pad_to_length - len(msg_bytes))
        self.device.write(0x03, msg_bytes)

    def get_default_keymap(self) -> Keymap:
        # this is an instance method, because it possibly depends
        # on exact keyboard model

        # TODO: models with a numpad
        return Keymap([  # noqa
            Key.ESC,    Key.NONE,   Key.F1,     Key.F2,     Key.F3,     Key.F4,     Key.F5,
            Key.F6,     Key.F7,     Key.F8,     Key.F9,     Key.F10,    Key.F11,    Key.F12,
            Key.PSCR,   Key.SLCK,   Key.PAUSE,  Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.GRAVE,  Key._1,     Key._2,     Key._3,     Key._4,     Key._5,     Key._6,
            Key._7,     Key._8,     Key._9,     Key._0,     Key.MINUS,  Key.EQUAL,  Key.BSPACE,
            Key.INSERT, Key.HOME,   Key.PGUP,   Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.TAB,    Key.Q,      Key.W,      Key.E,      Key.R,      Key.T,      Key.Y,
            Key.U,      Key.I,      Key.O,      Key.P,      Key.LBRC,   Key.RBRC,   Key.BSLASH,
            Key.DELETE, Key.END,    Key.PGDOWN, Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.CAPS,   Key.A,      Key.S,      Key.D,      Key.F,      Key.G,      Key.H,
            Key.J,      Key.K,      Key.L,      Key.SCOLON, Key.QUOTE,  Key.NONE,   Key.ENTER,
            Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.LSHIFT, Key.NONE,   Key.Z,      Key.X,      Key.C,      Key.V,      Key.B,
            Key.N,      Key.M,      Key.COMMA,  Key.DOT,    Key.SLASH,  Key.NONE,   Key.RSHIFT,
            Key.NONE,   Key.UP,     Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.LCTRL,  Key.LGUI,   Key.LALT,   Key.NONE,   Key.NONE,   Key.NONE,   Key.SPACE,
            Key.NONE,   Key.NONE,   Key.NONE,   Key.RALT,   Key.FN,     Key.APP,    Key.RCTRL,
            Key.LEFT,   Key.DOWN,   Key.RIGHT,  Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

            Key.WINLOCK_WIN, Key.MAGIC_PADDING,
        ])

    def apply_keymap(self, keymap: Keymap):
        self._write(KeymapStartMessage())

        for i in range(Keymap.ROW_COUNT):
            self._write(KeymapRowMessage(i, keymap.get_row(i)))

        self._write(KeymapEndMessage())

    def enable_rgb(self):
        self._write(RgbStateMessage(RgbState.ON))

    def disable_rgb(self):
        self._write(RgbStateMessage(RgbState.OFF))

    def apply_rgb_effect(
        self,
        effect: RgbEffect = RgbEffect.PLAY,
        speed: int = 1,
        brightness: int = 9,
        reversed: bool = False,
        color1: int = 0xffffff,
        color2: int = 0xffffff,
        base_speed: int = 1,
    ):
        self._write(RgbStateMessage(RgbState.ON))

        self._write(RgbEffectMessage(
            effect=effect,
            speed=speed,
            brightness=brightness,
            reversed=reversed,
            color1=color1,
            color2=color2,
            base_speed=base_speed,
        ))

    def get_default_colormap(self):
        # this is an instance method, because it possibly depends
        # on exact keyboard model

        return Colormap([0x000000] * Colormap.ROW_LENGTH * Colormap.ROW_COUNT)

    def apply_colormap(self, colormap: Colormap):
        self._write(RgbStateMessage(RgbState.OFF))
        self._write(RgbColormapStartMessage())

        for i in range(Colormap.ROW_COUNT):
            self._write(RgbColormapRowMessage(i, colormap.get_row(i)))

        self._write(RgbColormapEndMessage())

    def get_layout(self) -> Layout:
        # this is an instance method, because it possibly depends
        # on exact keyboard model

        G = Layout.Group

        # TODO: models with a numpad
        return Layout(width=18.25, height=6.5, groups=[
            G(1), G(skip=1, x=1), G(4), G(x=0.5), G(4), G(x=0.5), G(4),
            G(x=0.25), G(3),
            G(skip=4),

            G(row=True, y=0.5), G(13), G(1, w=2),
            G(x=0.25), G(3),
            G(skip=4),

            G(row=True), G(1, w=1.5), G(12), G(1, w=1.5),
            G(x=0.25), G(3),
            G(skip=4),

            G(row=True), G(1, w=1.75), G(11), G(skip=1), G(1, w=2.25),
            G(skip=3),
            G(skip=4),

            G(row=True), G(1, w=2.25), G(skip=1), G(10), G(skip=1), G(1, w=2.75),  # noqa
            G(skip=1, x=1.25), G(1), G(skip=1),
            G(skip=4),

            G(row=True), G(3, w=1.25), G(skip=3), G(1, w=6.25), G(skip=3), G(4, w=1.25),  # noqa
            G(x=0.25), G(3),
            G(skip=4)
        ])
