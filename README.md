# Etch-a-PING: Raspberry Pi Pico Pong

`PING` is a MicroPython Pong-inspired game for a Raspberry Pi Pico with real potentiometer paddles, an ILI9225 SPI LCD, a MAX98357A I2S amplifier, and a momentary start button.

It boots to a title screen, plays with an Etch A Sketch-style grey-and-black look, uses classic Pong-like sound effects, and keeps score to 11 with win-by-2 rules.

## Documentation

- [Build tutorial](TUTORIAL.md)
- [Bill of materials](BOM.md)

## Features

- Raspberry Pi Pico / Pico W firmware in MicroPython
- ILI9225 LCD driver included
- Two analog potentiometer paddles
- MAX98357A I2S audio using RP2040 PIO
- Momentary start button
- Final score screen
- First to 11, win by 2
- Battery-power notes for TP4056/LiPo builds

## Quick Wiring Summary

| Device | Pico pins |
| --- | --- |
| ILI9225 LCD | `GP17`, `GP18`, `GP19`, `GP20`, `GP21`, `GP22` |
| Potentiometers | `GP26`, `GP27`, `3V3 OUT`, `GND` |
| MAX98357A amp | `GP10`, `GP11`, `GP12` |
| Start button | `GP13`, `GND` |

See [BOM.md](BOM.md) and [TUTORIAL.md](TUTORIAL.md) for the complete wiring tables.

## Install

1. Flash current MicroPython for Raspberry Pi Pico onto the Pico.
2. Open `main.py` in Thonny.
3. Save it to the Pico as `main.py`.
4. Reset the Pico or unplug/replug it.

## Tuning

- If the screen is only white, the backlight is on but the display is not receiving commands. Recheck `CS`, `RST`, `RS`, `CLK`, and `SDI`.
- For screen debugging, save `screen_test_ili9225.py` to the Pico as `main.py`. It uses only the screen pins and cycles full-screen colors.
- To make the game faster or slower, change the `time.sleep_ms(12)` line at the end of the game loop.

## Diagnostic Scripts

These helper files can be saved to the Pico as `main.py` while debugging:

- `screen_test_ili9225.py`: verifies the ILI9225 display wiring.
- `audio_test.py`: verifies the MAX98357A audio wiring.
- `screen_wire_check.py`: pulses display pins for multimeter checks.

## Sources Checked

- Pico pinout: https://pico.pinout.xyz/
- MAX98357A pinout reference: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts
- ILI9225 register sequence reference: https://os.mbed.com/users/Arman92/code/ILI9225_SPI_TFT/file/cc93245bb6d0/TFT_22_ILI9225.cpp
