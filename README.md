RickRoll Wristband
==================

[![](https://img.youtube.com/vi/4qXFLblkhrk/0.jpg)](https://youtu.be/4qXFLblkhrk)

## What is it?

This is a project of a wearable watch with a secret
[rickroll spam](https://github.com/spacehuhn/esp8266_beaconSpam) Wi-Fi function based on a 
[LilyGo T-Wristband](https://www.lilygo.cc/products/t-wristband) device.
The watch uses deepsleep mode to reduce power consuption and also has
debug mode, that loads webrepl via Wi-Fi (station or access point mode).

This repository contains:
- Custom MicroPython-1.19.1 [firmware](https://github.com/zmactep/rickroll-wristband/tree/master/firmware) for ESP32
- Instruction how to build your own for different version
- A [code](https://github.com/zmactep/rickroll-wristband/tree/master/src) of watch app with rickroll function

## Special thanks

- MicroPython ([micropython/micropython](https://github.com/micropython/micropython))
- ST7789_mpy ([russhughes/st7789_mpy](https://github.com/russhughes/st7789_mpy))
