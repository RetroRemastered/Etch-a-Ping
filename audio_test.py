from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
import time


I2S_LRC = 28
I2S_BCLK = 27
I2S_DIN = 26
AUDIO_RATE = 16_000
AUDIO_VOLUME = 9000


@asm_pio(
    out_init=PIO.OUT_LOW,
    set_init=PIO.OUT_LOW,
    out_shiftdir=PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
    sideset_init=PIO.OUT_LOW,
)
def i2s_out():
    set(pins, 0).side(0)
    set(x, 15)
    label("left")
    out(pins, 1).side(0)
    nop().side(1)
    jmp(x_dec, "left").side(0)
    set(pins, 1).side(0)
    set(x, 15)
    label("right")
    out(pins, 1).side(0)
    nop().side(1)
    jmp(x_dec, "right").side(0)


audio = StateMachine(
    0,
    i2s_out,
    freq=AUDIO_RATE * 32 * 3,
    out_base=Pin(I2S_DIN),
    set_base=Pin(I2S_LRC),
    sideset_base=Pin(I2S_BCLK),
)
audio.active(1)


def tone(freq, duration_ms):
    sample_count = (AUDIO_RATE * duration_ms) // 1000
    period = max(2, AUDIO_RATE // freq)
    half = period // 2

    for i in range(sample_count):
        sample = AUDIO_VOLUME if i % period < half else -AUDIO_VOLUME
        if sample < 0:
            sample += 65536
        audio.put((sample << 16) | sample)


while True:
    print("440 Hz")
    tone(440, 800)
    time.sleep_ms(300)
    print("880 Hz")
    tone(880, 800)
    time.sleep_ms(800)
