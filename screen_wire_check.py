from machine import Pin
import time


PINS = (
    ("CS", 17),
    ("CLK", 18),
    ("SDI", 19),
    ("RS/DC", 20),
    ("RST", 21),
    ("LED", 22),
)


def pulse(pin_number, times):
    pin = Pin(pin_number, Pin.OUT)
    for _ in range(times):
        pin(1)
        time.sleep_ms(250)
        pin(0)
        time.sleep_ms(250)
    pin(0)


while True:
    for name, pin_number in PINS:
        print("Pulsing", name, "GP" + str(pin_number))
        pulse(pin_number, 6)
        time.sleep(2)
