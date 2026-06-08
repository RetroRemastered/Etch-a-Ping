# Bill of Materials

This build is a handheld Raspberry Pi Pico Pong console with real paddle controls, an ILI9225 color LCD, I2S audio, and a start button.

## Required Parts

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | Raspberry Pi Pico or Pico W | Headers recommended. |
| 1 | ILI9225 SPI LCD module | 176 x 220 display, red breakout board. |
| 2 | 10k potentiometers | Linear taper preferred for paddle controls. |
| 1 | MAX98357A I2S mono amplifier | Drives the speaker from Pico digital audio. |
| 1 | Small speaker | 4 ohm or 8 ohm speaker for the amp output. |
| 1 | Momentary pushbutton | Start button, normally open. |
| 1 | Breadboard, perfboard, or solderable prototyping board | Use whatever suits the enclosure. |
| Several | Jumper wires or hookup wire | 24-28 AWG works well. |

## Optional Battery Parts

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | 3.7V LiPo battery | Capacity depends on desired runtime. |
| 1 | TP4056 LiPo charger/protection board | Prefer a protected module with `B+`, `B-`, `OUT+`, and `OUT-`. |
| 1 | Locking on/off switch | Put this between TP4056 `OUT+` and Pico `VSYS`. |

## Tools

| Tool | Use |
| --- | --- |
| Soldering iron | Solder headers and wires. |
| Multimeter | Check continuity and voltages. |
| Computer with Thonny | Flash MicroPython and copy `main.py`. |
| USB cable | Pico programming and testing. |

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
