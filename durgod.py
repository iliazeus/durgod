import time
import usb


# These are the `idProduct`s of the USB spec
# TODO: ids of other supported keyboards
class KeyboardId:
    # ID 2f68:0082 Hoksi Technology DURGOD Taurus K320
    K320 = 0x0082

    # ID 2f68:0081 Hoksi Technology DURGOD Taurus K320 Nebula
    K320_NEBULA = 0x0081


# Names match with https://beta.docs.qmk.fm/using-qmk/simple-keycodes
# TODO: hypothetical numpad indices
class Matrix:
    HEIGHT = 16
    WIDTH = 8

    ESCAPE = ESC = 0 * WIDTH + 0
    F1 = 0 * WIDTH + 2
    F2 = 0 * WIDTH + 3
    F3 = 0 * WIDTH + 4
    F4 = 0 * WIDTH + 5
    F5 = 0 * WIDTH + 6
    F6 = 0 * WIDTH + 7

    F7 = 1 * WIDTH + 0
    F8 = 1 * WIDTH + 1
    F9 = 1 * WIDTH + 2
    F10 = 1 * WIDTH + 3
    F11 = 1 * WIDTH + 4
    F12 = 1 * WIDTH + 5
    PSCREEN = PSCR = 1 * WIDTH + 6
    SCROLLLOCK = SLCK = BRMD = 1 * WIDTH + 7

    PAUSE = PAUS = BRK = BRMU = 2 * WIDTH + 0
    GRAVE = GRV = ZKHK = 2 * WIDTH + 5
    ONE = 2 * WIDTH + 6
    TWO = 2 * WIDTH + 7

    THREE = 3 * WIDTH + 0
    FOUR = 3 * WIDTH + 1
    FIVE = 3 * WIDTH + 2
    SIX = 3 * WIDTH + 3
    SEVEN = 3 * WIDTH + 4
    EIGHT = 3 * WIDTH + 5
    NINE = 3 * WIDTH + 6
    ZERO = 3 * WIDTH + 7

    MINUS = MINS = 4 * WIDTH + 0
    EQUAL = EQL = 4 * WIDTH + 1
    BSPACE = BSPC = 4 * WIDTH + 2
    INSERT = INS = 4 * WIDTH + 3
    HOME = 4 * WIDTH + 4
    PGUP = 4 * WIDTH + 5

    TAB = 5 * WIDTH + 2
    Q = 5 * WIDTH + 3
    W = 5 * WIDTH + 4
    E = 5 * WIDTH + 5
    R = 5 * WIDTH + 6
    T = 5 * WIDTH + 7

    Y = 6 * WIDTH + 0
    U = 6 * WIDTH + 1
    I = 6 * WIDTH + 2
    O = 6 * WIDTH + 3
    P = 6 * WIDTH + 4
    LBRACKET = LBRC = 6 * WIDTH + 5
    RBRACKET = RBRC = 6 * WIDTH + 6
    BSLASH = BSLS = 6 * WIDTH + 7

    DELETE = DEL = 7 * WIDTH + 0
    END = 7 * WIDTH + 1
    PGDOWN = PGDN = 7 * WIDTH + 2
    CAPSLOCK = CLCK = CAPS = 7 * WIDTH + 7

    A = 8 * WIDTH + 0
    S = 8 * WIDTH + 1
    D = 8 * WIDTH + 2
    F = 8 * WIDTH + 3
    G = 8 * WIDTH + 4
    H = 8 * WIDTH + 5
    J = 8 * WIDTH + 6
    K = 8 * WIDTH + 7

    L = 9 * WIDTH + 0
    SCOLON = SCLN = 9 * WIDTH + 1
    QUOTE = QUOT = 9 * WIDTH + 2
    ENTER = ENT = 9 * WIDTH + 4

    LSHIFT = LSFT = 10 * WIDTH + 4
    Z = 10 * WIDTH + 6
    X = 10 * WIDTH + 7

    C = 11 * WIDTH + 0
    V = 11 * WIDTH + 1
    B = 11 * WIDTH + 2
    N = 11 * WIDTH + 3
    M = 11 * WIDTH + 4
    COMMA = COMM = 11 * WIDTH + 5
    DOT = 11 * WIDTH + 6
    SLASH = SLSH = 11 * WIDTH + 7

    RSHIFT = RSFT = 12 * WIDTH + 1
    UP = 12 * WIDTH + 3

    LCTRL = LCTL = 13 * WIDTH + 1
    LGUI = LCMD = LWIN = 13 * WIDTH + 2
    LALT = LOPT = 13 * WIDTH + 3
    SPACE = SPC = 13 * WIDTH + 7
    RALT = ROPT = 14 * WIDTH + 3
    FN = 14 * WIDTH + 4
    APPLICATION = APP = 14 * WIDTH + 5
    RCTRL = RCTL = 14 * WIDTH + 6
    LEFT = 14 * WIDTH + 7

    DOWN = 15 * WIDTH + 0
    RIGHT = 15 * WIDTH + 1
    WINLOCK_FLAGS = 15 * WIDTH + 6
    MAGIC_PADDING = 15 * WIDTH + 7


# https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
# Names match with https://beta.docs.qmk.fm/using-qmk/simple-keycodes
class Key:
    NONE = NO = 0x00000000

    FN = 0x00000001

    MAGIC_PADDING = 0x12345678

    # TODO: winlock flags
    # TODO: missing key codes

    MOD_LCTRL = MOD_LCTL = 0x0100
    MOD_LSHIFT = MOD_LSFT = 0x0200
    MOD_LALT = MOD_LOPT = 0x0400
    MOD_LGUI = MOD_LCMD = MOD_LWIN = 0x0800
    MOD_RCTRL = MOD_RCTL = 0x1000
    MOD_RSHIFT = MOD_RSFT = 0x2000
    MOD_RALT = MOD_ROPT = MOD_ALGR = 0x4000
    MOD_RGUI = MOD_RCMD = MOD_RWIN = 0x8000

    # since they are set in the keymap,
    # it makes sense to define these here
    WINLOCK_ALT_TAB = 0x01
    WINLOCK_ALT_F4 = 0x02
    WINLOCK_SHIFT_TAB = 0x03
    WINLOCK_WIN = 0x08

    A = 0x00040000
    B = 0x00050000
    C = 0x00060000
    D = 0x00070000
    E = 0x00080000
    F = 0x00090000
    G = 0x000a0000
    H = 0x000b0000
    I = 0x000c0000
    J = 0x000d0000
    K = 0x000e0000
    L = 0x000f0000
    M = 0x00100000
    N = 0x00110000
    O = 0x00120000
    P = 0x00130000
    Q = 0x00140000
    R = 0x00150000
    S = 0x00160000
    T = 0x00170000
    U = 0x00180000
    V = 0x00190000
    W = 0x001a0000
    X = 0x001b0000
    Y = 0x001c0000
    Z = 0x001d0000

    ONE = _1 = 0x001e0000
    TWO = _2 = 0x001f0000
    THREE = _3 = 0x00200000
    FOUR = _4 = 0x00210000
    FIVE = _5 = 0x00220000
    SIX = _6 = 0x00230000
    SEVEN = _7 = 0x00240000
    EIGHT = _8 = 0x00250000
    NINE = _9 = 0x00260000
    ZERO = _0 = 0x00270000

    ENTER = ENT = 0x00280000
    ESCAPE = ESC = 0x00290000
    BSPACE = BSPC = 0x002a0000
    TAB = 0x002b0000
    SPACE = SPC = 0x002c0000
    MINUS = MINS = 0x002d0000
    EQUAL = EQL = 0x002e0000
    LBRACKET = LBRC = 0x002f0000
    RBRACKET = RBRC = 0x00300000
    BSLASH = BSLS = 0x00310000
    NONUS_HASH = NUHS = 0x00320000
    SCOLON = SCLN = 0x00330000
    QUOTE = QUOT = 0x00340000
    GRAVE = GRV = ZKHK = 0x00350000
    COMMA = COMM = 0x00360000
    DOT = 0x00370000
    SLASH = SLSH = 0x00380000
    CAPSLOCK = CLCK = CAPS = 0x00390000

    F1 = 0x003a0000
    F2 = 0x003b0000
    F3 = 0x003c0000
    F4 = 0x003d0000
    F5 = 0x003e0000
    F6 = 0x003f0000
    F7 = 0x00400000
    F8 = 0x00410000
    F9 = 0x00420000
    F10 = 0x00430000
    F11 = 0x00440000
    F12 = 0x00450000

    PSCREEN = PSCR = 0x00460000
    SCROLLLOCK = SLCK = BRMD = 0x00470000
    PAUSE = PAUS = BRK = BRMU = 0x00480000
    INSERT = INS = 0x00490000
    HOME = 0x004a0000
    PGUP = 0x004b0000
    DELETE = DEL = 0x004c0000
    END = 0x004d0000
    PGDOWN = PGDN = 0x004e0000

    RIGHT = RGHT = 0x004f0000
    LEFT = 0x00500000
    DOWN = 0x00510000
    UP = 0x00520000

    NUMLOCK = NLCK = 0x00530000

    KP_SLASH = PSLS = 0x00540000
    KP_ASTERISK = PAST = 0x00550000
    KP_MINUS = PMNS = 0x00560000
    KP_PLUS = PPLS = 0x00570000
    KP_ENTER = PENT = 0x00580000

    KP_ONE = KP_1 = P1 = 0x00590000
    KP_TWO = KP_2 = P2 = 0x005a0000
    KP_THREE = KP_3 = P3 = 0x005b0000
    KP_FOUR = KP_4 = P4 = 0x005c0000
    KP_FIVE = KP_5 = P5 = 0x005d0000
    KP_SIX = KP_6 = P6 = 0x005e0000
    KP_SEVEN = KP_7 = P7 = 0x005f0000
    KP_EIGHT = KP_8 = P8 = 0x00600000
    KP_NINE = KP_9 = P_9 = 0x00610000
    KP_ZERO = KP_0 = P0 = 0x00620000

    KP_DOT = PDOT = 0x00630000

    NONUS_BSLASH = NUBS = 0x00640000

    APPLICATION = APP = 0x00650000

    POWER = 0x00660000

    KP_EQUAL = PEQL = 0x00670000

    F13 = 0x00680000
    F14 = 0x00690000
    F15 = 0x006a0000
    F16 = 0x006b0000
    F17 = 0x006c0000
    F18 = 0x006d0000
    F19 = 0x006e0000
    F20 = 0x006f0000
    F21 = 0x00700000
    F22 = 0x00710000
    F23 = 0x00720000
    F24 = 0x00730000

    EXECUTE = EXEC = 0x00740000
    HELP = 0x00750000
    MENU = 0x00760000
    SELECT = SLCT = 0x00770000
    STOP = 0x00780000
    AGAIN = AGIN = 0x00790000
    UNDO = 0x007a0000
    CUT = 0x007b0000
    COPY = 0x007c0000
    PASTE = PSTE = 0x007d0000
    FIND = 0x007e0000
    MUTE = 0x007f0000
    _VOLUP = 0x00800000
    _VOLDOWN = 0x00810000

    LOCKING_CAPS = LCAP = 0x00820000
    LOCKING_NUM = LNUM = 0x00830000
    LOCKING_SCROLL = LSCR = 0x00840000

    KP_COMMA = PCMM = 0x00850000
    KP_EQUAL_AS400 = 0x00860000

    INT1 = RO = 0x00870000
    INT2 = KANA = 0x00880000
    INT3 = JYEN = 0x00890000
    INT4 = HENK = 0x008a0000
    INT5 = MHEN = 0x008b0000
    INT6 = 0x008c0000
    INT7 = 0x008d0000
    INT8 = 0x008e0000
    INT9 = 0x008f0000

    LANG1 = HAEN = 0x00900000
    LANG2 = HANJ = 0x00910000
    LANG3 = 0x00920000
    LANG4 = 0x00930000
    LANG5 = 0x00940000
    LANG6 = 0x00950000
    LANG7 = 0x00960000
    LANG8 = 0x00970000
    LANG9 = 0x00980000

    ALT_ERASE = ERAS = 0x00990000

    SYSREQ = 0x009a0000
    CANCEL = 0x009b0000
    CLEAR = CLR = 0x009c0000
    PRIOR = 0x009d0000
    RETURN = 0x009e0000
    SEPARATOR = 0x009f0000
    OUT = 0x00a00000
    OPER = 0x00a10000
    CLEAR_AGAIN = 0x00a20000
    CRSEL = 0x00a30000
    EXSEL = 0x00a40000

    LCTRL = LCTL = 0x00e00000
    LSHIFT = LSFT = 0x00e10000
    LALT = LOPT = 0x00e20000
    LGUI = LCMD = LWIN = 0x00e30000
    RCTRL = RCTL = 0x00e40000
    RSHIFT = RSFT = 0x00e50000
    RALT = ROPT = ALGR = 0x00e60000
    RGUI = RCMD = RWIN = 0x00e70000

    SYSTEM_POWER = PWR = None
    SYSTEM_SLEEP = SLEP = 0x00f80000
    SYSTEM_WAKE = WAKE = 0x00f90000

    AUDIO_MUTE = MUTE = 0x00ef0000
    AUDIO_VOL_UP = VOLU = 0x00ed0000
    AUDIO_VOL_DOWN = VOLD = 0x00ee0000

    MEDIA_NEXT_TRACK = MNXT = 0x00eb0000
    MEDIA_PREV_TRACK = MPRV = 0x00ea0000
    MEDIA_STOP = MSTP = 0x00e90000
    MEDIA_PLAY_PAUSE = MPLY = 0x00e80000
    MEDIA_SELECT = MSEL = None
    MEDIA_EJECT = EJCT = 0x00ec0000

    MAIL = None
    CALCULATOR = CALC = 0x00fb0000
    MY_COMPUTER = MYCM = None

    WWW_SEARCH = WSCH = 0x00f40000
    WWW_HOME = WHOM = 0x00f00000
    WWW_BACK = WBAK = 0x00f10000
    WWW_FORWARD = WFWD = 0x00f20000
    WWW_STOP = WSTP = 0xf3
    WWW_REFRESH = WREF = 0x00fa0000
    WWW_FAVORITES = WFAV = None

    MEDIA_FAST_FORWARD = MFFD = None
    MEDIA_REWIND = MRWD = None

    BRIGHTNESS_UP = BRIU = None
    BRIGHTNESS_DOWN = BRID = None


class RgbEffect:
    PLAY = 0x0
    PAUSE = 0x1
    RAINBOW = 0x2
    TWO_COLORS = 0x3
    CHRISTMAS = 0x4
    TRACKS = 0x5
    LASERS = 0x6
    WAVES = 0x7
    SNAKE = 0x8
    TYPING_SPEED = 0x9


class Keyboard:
    KEYMAP_ENTRY_LENGTH = 8
    KEYMAP_ENTRY_COUNT = 16

    DEFAULT_KEYMAP = [  # noqa
        Key.ESC,    Key.NONE,   Key.F1,     Key.F2,     Key.F3,     Key.F4,     Key.F5,     Key.F6,
        Key.F7,     Key.F8,     Key.F9,     Key.F10,    Key.F11,    Key.F12,    Key.PSCR,   Key.SLCK,
        Key.PAUSE,  Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

                                                                    Key.GRAVE,  Key._1,     Key._2,
        Key._3,     Key._4,     Key._5,     Key._6,     Key._7,     Key._8,     Key._9,     Key._0,
        Key.MINUS,  Key.EQUAL,  Key.BSPACE, Key.INSERT, Key.HOME,   Key.PGUP,   Key.NONE,   Key.NONE,
        Key.NONE,   Key.NONE,

                                Key.TAB,    Key.Q,      Key.W,      Key.E,      Key.R,      Key.T,
        Key.Y,      Key.U,      Key.I,      Key.O,      Key.P,      Key.LBRC,   Key.RBRC,   Key.BSLASH,
        Key.DELETE, Key.END,    Key.PGDOWN, Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

                                                                                            Key.CAPS,
        Key.A,      Key.S,      Key.D,      Key.F,      Key.G,      Key.H,      Key.J,      Key.K,
        Key.L,      Key.SCOLON, Key.QUOTE,  Key.NONE,   Key.ENTER,  Key.NONE,   Key.NONE,   Key.NONE,
        Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

                                                        Key.LSHIFT, Key.NONE,   Key.Z,      Key.X,
        Key.C,      Key.V,      Key.B,      Key.N,      Key.M,      Key.COMMA,  Key.DOT,    Key.SLASH,
        Key.NONE,   Key.RSHIFT, Key.NONE,   Key.UP,     Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,
        Key.NONE,

                    Key.LCTRL,  Key.LGUI,   Key.LALT,   Key.NONE,   Key.NONE,   Key.NONE,   Key.SPACE,
        Key.NONE,   Key.NONE,   Key.NONE,   Key.RALT,   Key.FN,     Key.APP,    Key.RCTRL,  Key.LEFT,
        Key.DOWN,   Key.RIGHT,  Key.NONE,   Key.NONE,   Key.NONE,   Key.NONE,

        Key.WINLOCK_WIN, Key.MAGIC_PADDING,
    ]

    COLORMAP_ENTRY_LENGTH = 14
    COLORMAP_ENTRY_COUNT = 9

    # channel order: 0xrrggbb
    # order is the same as in keymap, but in groups of 14
    DEFAULT_COLORMAP = [0x000000] * \
        COLORMAP_ENTRY_LENGTH * COLORMAP_ENTRY_COUNT

    def _pad_to_64(list):
        return list + [0x00] * (64 - len(list))

    def find(product_id=None, vendor_id=0x2f68):
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

    def __init__(self, device, keymap=None, colormap=None):
        self.device = device
        self.keymap = keymap or Keyboard.DEFAULT_KEYMAP[:]
        self.colormap = colormap or Keyboard.DEFAULT_COLORMAP[:]

        config = device.get_active_configuration()

        interface = usb.util.find_descriptor(config, bInterfaceSubClass=0x00)
        if self.device.is_kernel_driver_active(interface.index):
            self.device.detach_kernel_driver(interface.index)

    def _write(self, msg, pad_length=None):
        if pad_length is not None:
            msg = msg + [0x00] * (pad_length - len(msg))
        self.device.write(0x03, msg)

    def _write_keymap_start(self):
        self._write([0x03, 0x05, 0x80, 0x04, 0xff], pad_length=64)

    def _write_keymap_entry(self, index):
        msg = [0x03, 0x05, 0x81, 0x0f]
        msg += list(index.to_bytes(4, byteorder='little'))

        length = Keyboard.KEYMAP_ENTRY_LENGTH
        entry = self.keymap[length * index:length * (index + 1)]

        for key in entry:
            msg += list(key.to_bytes(4, byteorder='little'))

        self._write(msg, pad_length=64)

    def _write_keymap_end(self):
        self._write([0x03, 0x05, 0x82], pad_length=64)

    def apply_keymap(self):
        self._write_keymap_start()

        for index in range(0, Keyboard.KEYMAP_ENTRY_COUNT):
            self._write_keymap_entry(index)

        self._write_keymap_end()

    def _write_rgb_state(self, state):
        msg = [0x03, 0x06, 0x86, state & 0xff]
        self._write(msg, pad_length=64)

    def _write_rgb_effect(
        self,
        mode,
        direction,
        color1,
        speed,
        brightness,
        base_speed,
        color2,
    ):
        msg = [0x03, 0x06, 0x80]
        msg += [mode & 0xff]
        msg += [direction & 0xff]
        msg += [0x00]
        msg += list(color1.to_bytes(3, byteorder='big'))
        msg += [speed & 0xff]
        msg += [brightness & 0xff]
        msg += [base_speed & 0xff]
        msg += list(color2.to_bytes(3, byteorder='big'))

        self._write(msg, pad_length=64)

    def _write_rgb_brightness(self, brightness):
        msg = [0x03, 0x06, 0x82, brightness & 0xff]
        self._write(msg, pad_length=64)

    def _write_rgb_speed(self, speed):
        msg = [0x03, 0x06, 0x83, speed & 0xff]
        self._write(msg, pad_length=64)

    def _write_rgb_colormap_start(self):
        self._write([0x03, 0x19, 0x66], pad_length=64)

    def _write_rgb_colormap_entry(self, index):
        msg = [0x03, 0x18, 0x08]
        msg += [index & 0xff]

        length = Keyboard.COLORMAP_ENTRY_LENGTH
        entry = self.colormap[length * index: length * (index + 1)]

        for key in entry:
            msg += list(key.to_bytes(3, byteorder='big'))

        self._write(msg, pad_length=64)

    def _write_rgb_colormap_end(self):
        self._write([0x03, 0x19, 0x88], pad_length=64)

    def disable_rgb(self):
        self._write_rgb_state(1)

    def apply_rgb_effect(
        self,
        effect=RgbEffect.PLAY,
        direction=0,
        color1=0xffffff,
        speed=2,
        brightness=9,
        base_speed=1,
        color2=0xffffff,
    ):
        self._write_rgb_state(0)
        self._write_rgb_effect(
            mode=effect,
            direction=direction,
            color1=color1,
            speed=speed,
            brightness=brightness,
            base_speed=base_speed,
            color2=color2,
        )

    def apply_rgb_colormap(self):
        self._write_rgb_state(1)
        self._write_rgb_colormap_start()

        for index in range(0, Keyboard.COLORMAP_ENTRY_COUNT):
            self._write_rgb_colormap_entry(index)

        self._write_rgb_colormap_end()


if __name__ == "__main__":
    kb = Keyboard.find()

    if kb is None:
        raise ValueError('device not found')

    # kb.keymap[Matrix.SCROLLLOCK] = Key.MOD_LSHIFT | Key.Z
    # kb.apply_keymap()

    kb.colormap[Matrix.Z] = 0xff0000
    kb.apply_rgb_colormap()
    time.sleep(0.5)

    kb.colormap[Matrix.Z] = 0x00ff00
    kb.apply_rgb_colormap()
    time.sleep(0.5)

    kb.colormap[Matrix.Z] = 0x0000ff
    kb.apply_rgb_colormap()
    time.sleep(0.5)

    kb.apply_rgb_effect()

    # kb.apply_rgb_effect(RgbMode.WAVES, speed=2, brightness=4)
