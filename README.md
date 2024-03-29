This is a partial reverse-engineering of the protocol used by the [Durgod Zeus Engine], with the aim of being used on the platforms not supported by the Zeus Engine itself (which only supports Windows).

I don't currently own a Durgod keyboard anymore, so I'm not able to work on this. If you have an improvement idea, feel free to fork this!

Features that are currently supported:

- remapping of the "custom layer" toggled by `Fn + F12`
- very basic RGB control

Features that I want to implement (if possible):

- macros
- per-key RGB control

I use [QEMU] to run the Zeus Engine on a Windows VM, [Wireshark] to capture USB data, and [pyusb] to communicate with the board.

I only tested it on Linux, with my Durgod Taurus K320 Nebula (the tenkeyless RGB one). But it should work on all platforms supported by Python 3 and pyusb, and may probably work with other Durgod Taurus keyboards. In particular, the custom layer remapping feature should work an all of them.

This project will most probably only have features that the Zeus Engine has. If you have an STM32-based Taurus, a more feature-rich alternative would be flashing with the [QMK firmware].

[durgod zeus engine]: https://www.durgod.com/Durgod-Zeus-Engine?_l=en
[qemu]: https://www.qemu.org/
[wireshark]: https://www.wireshark.org/
[pyusb]: https://github.com/pyusb/pyusb
[qmk firmware]: https://github.com/qmk/qmk_firmware/tree/master/keyboards/durgod/
