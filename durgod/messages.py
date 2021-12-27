import abc
import struct

from .constants import *


class Message(abc.ABC):
    """A base class for all messages sent to a keyboard"""

    @abc.abstractmethod
    def pack(self) -> bytes:
        """Pack a message into bytes for sending through USB."""

        pass


class KeymapStartMessage(Message):
    """Sent on changing the custom layer mapping, before the actual data."""

    def __init__(self):
        self.opcode = b'\x03\x05\x80\x04'
        self.magic = 0xff

    def pack(self) -> bytes:
        return struct.pack('< 4s i', self.opcode, self.magic)


class KeymapRowMessage(Message):
    """Sent on changing the custom layer mapping, contains actual mapping data."""

    def __init__(
        self,
        index: int,
        keys: list[Key],
    ):
        assert 0 <= index <= 15
        assert len(keys) == 8

        self.opcode = b'\x03\x05\x81\x0f'
        self.index = index
        self.keys = keys

    def pack(self) -> bytes:
        entries = b''.join(map(lambda k: k.to_bytes(4, 'little'), self.keys))

        return struct.pack(
            '< 4s i 32s',
            self.opcode,
            self.index,
            entries,
        )


class KeymapEndMessage(Message):
    """Sent on changing the custom layer mapping, after all the data."""

    def __init__(self):
        self.opcode = b'\x03\x05\x82\x00'

    def pack(self):
        return struct.pack('< 4s', self.opcode)


class RgbStateMessage(Message):
    """Sent to enable or disable RGB lighting."""

    def __init__(self, state: RgbState):
        self.opcode = b'\x03\x06\x86'
        self.stop = state

    def pack(self) -> bytes:
        return struct.pack('< 3s b', self.opcode, self.stop)


class RgbEffectMessage(Message):
    """Sent to start a particular RGB lighting effect."""

    def __init__(
        self,
        effect: RgbEffect,
        reversed: bool,
        color1: int,
        speed: int,
        brightness: int,
        base_speed: int,
        color2: int,
    ):
        assert color1 & 0xffffff == color1
        assert 1 <= speed <= 3
        assert 1 <= brightness <= 9
        assert color2 & 0xffffff == color1

        self.opcode = b'\x03\x06\x80'
        self.effect = effect
        self.reversed = reversed
        self.color1 = color1
        self.speed = speed
        self.brightness = brightness
        self.base_speed = base_speed
        self.color2 = color2

    def pack(self) -> bytes:
        return struct.pack(
            '< 3s b ? x 3s b b b 3s',
            self.opcode,
            self.effect,
            self.reversed,
            self.color1.to_bytes(3, 'big'),
            self.speed,
            self.brightness,
            self.base_speed,
            self.color2.to_bytes(3, 'big'),
        )


class RgbBrightnessMessage(Message):
    """Sent to control overall RGB brighness."""

    def __init__(self, brightness: int):
        assert 1 <= brightness <= 9

        self.opcode = b'\x03\x06\x82'
        self.brightness = brightness

    def pack(self) -> bytes:
        return struct.pack('< 3s b', self.opcode, self.brightness)


class RgbSpeedMessage(Message):
    """Sent to control RGB effect speed."""

    def __init__(self, speed: int):
        assert 1 <= speed <= 3

        self.opcode = b'\x03\x06\x83'
        self.speed = speed

    def pack(self) -> bytes:
        return struct.pack('< 3s b', self.opcode, self.speed)


class RgbColormapStartMessage(Message):
    """Sent before the data for the per-key RGB lighting."""

    def __init__(self):
        self.opcode = b'\x03\x19\x66'

    def pack(self) -> bytes:
        return struct.pack('< 3s', self.opcode)


class RgbColormapRowMessage(Message):
    """Sent to control the per-key RGB lighting."""

    def __init__(self, index: int, colors: list[int]):
        assert 0 <= index <= 9
        assert len(colors) == 14

        self.opcode = b'\x03\x18\x08'
        self.index = index
        self.colors = colors

    def pack(self) -> bytes:
        entries = b''.join(map(lambda c: c.to_bytes(3, 'big'), self.colors))

        return struct.pack(
            '< 3s b 42s',
            self.opcode,
            self.index,
            entries,
        )


class RgbColormapEndMessage(Message):
    """Sent after the data for the per-key RGB lighting."""

    def __init__(self):
        self.opcode = b'\x03\x19\x88'

    def pack(self) -> bytes:
        return struct.pack('< 3s', self.opcode)
