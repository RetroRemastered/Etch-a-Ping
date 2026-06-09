# Bill of Materials

This build is a handheld Raspberry Pi Pico Pong console with real paddle controls, an ILI9225 color LCD, I2S audio, and a start button.

## Required Parts

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | Raspberry Pi Pico | No need for Pico 2. |
| 1 | ILI9225 SPI LCD module | 176 x 220 display, red breakout board. |
| 2 | 10k potentiometers | Linear taper preferred for paddle controls. |
| 1 | MAX98357A I2S mono amplifier | Drives the speaker from Pico digital audio. |
| 1 | Game Boy DMG speaker | 8 ohm speaker for the amp output. |
| 1 | Momentary pushbutton | Start button. |
| 1 | 3.7V LiPo battery | Small Battery that actually fits. |
| 1 | TP4056 LiPo charger/protection board | USB-C version. |
| 1 | Locking on/off switch | Put this between TP4056 `OUT+` and Pico `VSYS`. |
| Several | Jumper wires or hookup wire | 30 AWG is what I use. |

## Case Hardware

| Qty | Part | Notes |
| --- | --- | --- |
| 4 | `M2x4mm` machine screws | Used to mount the screen. |
| 4 | `M2x4x3.2` heat-set inserts | Used in the printed case so the back can screw on cleanly. |
| 4 | `M2x8mm` machine screws | Used with the heat-set inserts to close the two case halves. |

## Part Links

Add direct purchase links here for the exact parts used in your build.

| Part | Link |
| --- | --- |
| Raspberry Pi Pico or Pico W | https://amzn.to/4ftIaCY |
| ILI9225 SPI LCD module | https://amzn.to/4e5MO7L |
| 10k potentiometers | https://amzn.to/4dSDFkc |
| MAX98357A I2S mono amplifier | https://amzn.to/4ogg4NH |
| Game Boy DMG speaker | https://amzn.to/3S9yOTa |
| Momentary pushbutton | https://amzn.to/4um4aTU |
| 3.7V LiPo battery | https://amzn.to/49N2Diw |
| TP4056 LiPo charger/protection board | https://amzn.to/3RUsTRW |
| Locking on/off switch | https://amzn.to/4xhQewU |
| Hookup wire / jumper wire | https://amzn.to/3S8yR1x |
| `M2x4mm` screen screws |  |
| `M2x4x3.2` heat-set inserts |  |
| `M2x8mm` case screws |  |

## Tools

| Tool | Use |
| --- | --- |
| Soldering iron | Solder headers and wires. |
| Multimeter | Check continuity and voltages. |
| Computer with Thonny | Flash MicroPython and copy `main.py`. |
| USB cable | Pico programming and testing. |
| Heat-set insert tip or soldering iron | Install threaded inserts into the printed case. |

## Pin Summary

### ILI9225 LCD

| LCD signal | Pico pin |
| --- | --- |
| VCC | `3V3 OUT` |
| GND | `GND` |
| LED | `GP22` |
| CLK | `GP18` |
| SDI | `GP19` |
| RS / DC | `GP20` |
| RST | `GP21` |
| CS | `GP17` |

### Potentiometers

| Control | Pot outer leg | Pot wiper | Pot other outer leg |
| --- | --- | --- | --- |
| Left paddle | `3V3 OUT` | `GP26 / ADC0` | `GND` |
| Right paddle | `3V3 OUT` | `GP27 / ADC1` | `GND` |

If a paddle moves backward, swap that potentiometer's two outer-leg wires.

### MAX98357A Amplifier

| MAX98357A signal | Pico pin |
| --- | --- |
| Vin | `3V3 OUT` or `VSYS` |
| GND | `GND` |
| LRC | `GP10` |
| BCLK | `GP11` |
| DIN | `GP12` |

Connect the speaker to the amplifier screw terminal output. Do not connect a speaker directly to a Pico GPIO pin.

### Start Button

| Button leg | Pico pin |
| --- | --- |
| One side | `GP13` |
| Other side | `GND` |

The firmware uses the Pico internal pull-up resistor.
