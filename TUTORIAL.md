# Build Tutorial

This tutorial walks through building `PING`, a Pong-inspired game for Raspberry Pi Pico with real potentiometer paddles, an ILI9225 LCD, and MAX98357A audio.

## 1. Flash MicroPython

1. Download the latest MicroPython UF2 for your board:
   - Raspberry Pi Pico: https://micropython.org/download/RPI_PICO/
   - Raspberry Pi Pico W: https://micropython.org/download/RPI_PICO_W/
2. Hold the Pico `BOOTSEL` button while plugging it into USB.
3. Copy the downloaded `.uf2` file to the `RPI-RP2` drive.
4. The Pico will reboot into MicroPython.

## 2. Wire the Display

Wire the ILI9225 display first. The screen is the trickiest part, so double-check each connection before adding everything else.

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

If the screen stays white after installing the game, the backlight is on but the display controller is not receiving commands. Check continuity on `CS`, `CLK`, `SDI`, `RS`, and `RST`.

## 3. Wire the Paddles

Each potentiometer is wired as a voltage divider.

| Control | Pot outer leg | Pot wiper | Pot other outer leg |
| --- | --- | --- | --- |
| Left paddle | `3V3 OUT` | `GP26 / ADC0` | `GND` |
| Right paddle | `3V3 OUT` | `GP27 / ADC1` | `GND` |

Use `3V3 OUT`, not `3V3_EN`. The `3V3_EN` pin is an enable pin for the Pico regulator, not a sensor power rail.

## 4. Wire the Audio

Wire the MAX98357A I2S amplifier.

| MAX98357A signal | Pico pin |
| --- | --- |
| Vin | `3V3 OUT` or `VSYS` |
| GND | `GND` |
| LRC | `GP10` |
| BCLK | `GP11` |
| DIN | `GP12` |

Connect the speaker to the amplifier output terminals. If the amp is silent, connect `SD` to `Vin` to force the amp on.

## 5. Wire the Start Button

Wire a normally open momentary switch:

| Button leg | Pico pin |
| --- | --- |
| One side | `GP13` |
| Other side | `GND` |

No external resistor is required because the firmware uses the Pico internal pull-up.

## 6. Install the Game

1. Open `main.py` in Thonny.
2. Choose `File` -> `Save As...`.
3. Select `Raspberry Pi Pico`.
4. Save the file as exactly `main.py`.
5. Unplug and reconnect the Pico, or restart the backend in Thonny.

On boot, the screen shows `PING`. Press the start button to begin.

## 7. Gameplay

- The first player to reach 11 wins, but they must win by 2 points.
- The score is hidden during active play.
- After each point, the score appears briefly while the paddles can still move.
- After a match ends, the final score remains on screen until the start button is pressed.

## 8. Battery Power Option

For a portable build, use a protected TP4056 charger board with a single-cell LiPo.

Basic wiring:

| Connection | Destination |
| --- | --- |
| LiPo red | TP4056 `B+` |
| LiPo black | TP4056 `B-` |
| TP4056 `OUT+` | Locking switch, then Pico `VSYS` |
| TP4056 `OUT-` | Pico `GND` |

Do not connect battery power to `3V3 OUT`. Use `VSYS`.

Charge the LiPo through the TP4056 USB port. For small LiPo cells, make sure the charger current is appropriate for the battery capacity.

## Troubleshooting

### Screen is white

The backlight is powered, but the display controller is not receiving commands. Check `VCC`, `GND`, `CS`, `CLK`, `SDI`, `RS`, and `RST`.

### Audio is silent

Check `Vin`, `GND`, `LRC`, `BCLK`, `DIN`, speaker wiring, and the amp `SD` pin.

### Paddles move backward

Swap the two outer legs of that potentiometer.

### Paddles feel too sensitive

Lower `PADDLE_SENSITIVITY` in `main.py`.

### Ball speed needs tuning

Change `BALL_SPEED` and `SERVE_SPEED` in `main.py`.
