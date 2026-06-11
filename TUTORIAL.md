# Build Tutorial

This written guide follows the same general flow as the video walkthrough: gather the parts, print the enclosure, wire the electronics in small sections, load the firmware, then close it up and play.

You can follow along with me as I build it in this video here: https://youtu.be/AFBS6jwd1_I

`PING` is a Pong-inspired game for Raspberry Pi Pico with real potentiometer paddles, an ILI9225 LCD, MAX98357A audio, a start button, and LiPo battery power.

## 1. Print the Enclosure

The printable parts are in the [`3d-print`](3d-print) folder:

| File | Use |
| --- | --- |
| [`etch-a-ping-front.stl`](3d-print/etch-a-ping-front.stl) | Front shell with the screen and controls. |
| [`etch-a-ping-back.stl`](3d-print/etch-a-ping-back.stl) | Back shell. |
| [`etch-a-ping-knob.stl`](3d-print/etch-a-ping-knob.stl) | Potentiometer knob. Print two knobs. |

Print one front, one back, and two knobs. Test-fit the screen, pots, start button, switch, speaker, Pico, battery, charger board, four `M2x4x3.2` heat-set inserts, four `M2x4mm` screen screws, and four `M2x8mm` case screws before soldering the final wiring. The case is tight, so it is easier to fix fit issues before the wires are attached.

Install the four `M2x4x3.2` heat-set inserts before final assembly. Use a heat-set insert tip or a soldering iron set to a moderate temperature, press each insert in slowly, and let the plastic cool before test-fitting the `M2x8mm` screws. The inserts should sit flush and straight so the back shell closes without stress.

## 2. Flash MicroPython

1. Download the latest MicroPython UF2 for your board:
   - Raspberry Pi Pico: https://micropython.org/download/RPI_PICO/
   - Raspberry Pi Pico W: https://micropython.org/download/RPI_PICO_W/
2. Hold the Pico `BOOTSEL` button while plugging it into USB.
3. Copy the downloaded `.uf2` file to the `RPI-RP2` drive.
4. The Pico will reboot into MicroPython.

After MicroPython is installed, open Thonny and make sure you can connect to the Pico.

## 3. Install the Game

1. Open [`main.py`](main.py) in Thonny.
2. Choose `File` -> `Save As...`.
3. Select `Raspberry Pi Pico`.
4. Save the file as exactly `main.py`.
5. Unplug and reconnect the Pico, or restart the backend in Thonny.

On boot, the screen shows `PING`. Press the start button to begin once the build is wired.

## 4. Prep the Main Parts

Before wiring everything together, mount or test-fit these parts in the printed front shell:

- ILI9225 display
- Two 10k potentiometers
- Momentary start button
- Locking power switch
- Speaker
- Heat-set inserts and case screws

Keep the Pico, MAX98357A amp, TP4056 charger board, and battery loose until the wiring is mostly finished. This makes it easier to route wires without fighting the case.

## 5. Wire the Display

Wire the ILI9225 display first. The display is the trickiest part of the build, so take your time here.

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

If the screen stays white after installing the game, the backlight is powered but the display controller is not receiving commands. Check continuity on `CS`, `CLK`, `SDI`, `RS`, and `RST`.

## 6. Wire the Paddles

Each potentiometer is wired as a voltage divider.

| Control | Pot outer leg | Pot wiper | Pot other outer leg |
| --- | --- | --- | --- |
| Left paddle | `3V3 OUT` | `GP26 / ADC0` | `GND` |
| Right paddle | `3V3 OUT` | `GP27 / ADC1` | `GND` |

Use `3V3 OUT`, not `3V3_EN`. The `3V3_EN` pin controls the Pico regulator and should not be used as the power rail for the potentiometers.

If a paddle moves backward later, swap that potentiometer's two outer-leg wires.

## 7. Wire the Audio

Wire the MAX98357A I2S amplifier.

| MAX98357A signal | Pico pin |
| --- | --- |
| Vin | `3V3 OUT` or `VSYS` |
| GND | `GND` |
| LRC | `GP10` |
| BCLK | `GP11` |
| DIN | `GP12` |

Connect the speaker to the amplifier output terminals. Do not connect the speaker directly to the Pico.

If the amp is silent, connect the amp `SD` pin to `Vin` to force the amp on.

## 8. Wire the Start Button

Wire the normally open momentary switch:

| Button leg | Pico pin |
| --- | --- |
| One side | `GP13` |
| Other side | `GND` |

No external resistor is required because the firmware uses the Pico internal pull-up.

## 9. Wire Battery Power

Use a protected TP4056 charger board with a single-cell 3.7V LiPo.

| Connection | Destination |
| --- | --- |
| LiPo red | TP4056 `B+` |
| LiPo black | TP4056 `B-` |
| TP4056 `OUT+` | Locking switch, then Pico `VSYS` |
| TP4056 `OUT-` | Pico `GND` |

Do not connect battery power to `3V3 OUT`. Use `VSYS`.

The locking switch goes on the positive output side, between TP4056 `OUT+` and Pico `VSYS`. Charge the battery through the TP4056 USB port, not through the Pico USB port.

For small LiPo cells, make sure the TP4056 charge current is appropriate for the battery capacity.

## 10. Final Assembly

Once the screen, controls, audio, and battery wiring all work:

1. Place the screen into the front shell.
2. Secure the screen with four `M2x4mm` screws.
3. Install the potentiometers and knobs.
4. Install the start button and locking power switch.
5. Position the speaker so it is not pressing hard into the screen or Pico.
6. Secure the Pico, amplifier, TP4056 board, and battery.
7. Route wires so the back shell does not pinch them.
8. Close the case with four `M2x8mm` screws threaded into the heat-set inserts.

Power it on with the locking switch, wait for the `PING` title, then press the start button.

## 11. Gameplay

- The first player to reach 11 wins, but they must win by 2 points.
- The score is hidden during active play.
- After each point, the score appears briefly while the paddles can still move.
- After a match ends, the final score remains on screen until the start button is pressed.

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
