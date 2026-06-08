from machine import Pin, SoftSPI
import time


LCD_LED = 22

# Your stated pins. This finder tests whether any of these three are swapped.
CONTROL_PINS = (17, 20, 21)  # CS, RS/DC, RST in some order

# Your stated SPI pins, plus the common accidental swap.
SPI_PIN_PAIRS = (
    (18, 19),  # CLK, SDI
    (19, 18),  # swapped CLK, SDI
)

WIDTH = 160
HEIGHT = 128

RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
WHITE = 0xFFFF
BLACK = 0x0000
YELLOW = 0xFFE0
MAGENTA = 0xF81F
CYAN = 0x07FF
COLORS = (
    ("RED", RED),
    ("GREEN", GREEN),
    ("BLUE", BLUE),
    ("YELLOW", YELLOW),
    ("MAGENTA", MAGENTA),
    ("CYAN", CYAN),
    ("WHITE", WHITE),
)


def blink(count, on_ms=120, off_ms=120):
    led = Pin(LCD_LED, Pin.OUT)
    for _ in range(count):
        led(0)
        time.sleep_ms(on_ms)
        led(1)
        time.sleep_ms(off_ms)
    time.sleep_ms(500)


def permutations(items):
    for a in items:
        for b in items:
            for c in items:
                if a != b and b != c and a != c:
                    yield a, b, c


class ST7735Probe:
    def __init__(self, sck_pin, mosi_pin, cs_pin, dc_pin, rst_pin):
        self.spi = SoftSPI(
            baudrate=300_000,
            polarity=0,
            phase=0,
            sck=Pin(sck_pin),
            mosi=Pin(mosi_pin),
            miso=Pin(16),
        )
        self.cs = Pin(cs_pin, Pin.OUT, value=1)
        self.dc = Pin(dc_pin, Pin.OUT, value=0)
        self.rst = Pin(rst_pin, Pin.OUT, value=1)

    def cmd(self, command, data=None):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([command]))
        if data:
            self.dc(1)
            self.spi.write(data)
        self.cs(1)

    def init(self):
        self.cs(1)
        self.rst(1)
        time.sleep_ms(100)
        self.rst(0)
        time.sleep_ms(150)
        self.rst(1)
        time.sleep_ms(300)

        self.cmd(0x01)
        time.sleep_ms(300)
        self.cmd(0x11)
        time.sleep_ms(300)
        self.cmd(0x3A, b"\x05")
        self.cmd(0x36, b"\x60")
        self.cmd(0x29)
        time.sleep_ms(300)

    def fill(self, color):
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo]) * WIDTH
        self.cmd(0x2A, bytes([0, 0, 0, WIDTH - 1]))
        self.cmd(0x2B, bytes([0, 0, 0, HEIGHT - 1]))
        self.cmd(0x2C)
        self.cs(0)
        self.dc(1)
        for _ in range(HEIGHT):
            self.spi.write(row)
        self.cs(1)


Pin(LCD_LED, Pin.OUT, value=1)
blink(4)

attempt = 1
while True:
    for sck_pin, mosi_pin in SPI_PIN_PAIRS:
        for cs_pin, dc_pin, rst_pin in permutations(CONTROL_PINS):
            print(
                "Attempt",
                attempt,
                "CLK",
                sck_pin,
                "SDI",
                mosi_pin,
                "CS",
                cs_pin,
                "RS/DC",
                dc_pin,
                "RST",
                rst_pin,
            )
            lcd = ST7735Probe(sck_pin, mosi_pin, cs_pin, dc_pin, rst_pin)
            lcd.init()
            for name, color in COLORS:
                print("Attempt", attempt, "drawing", name)
                lcd.fill(color)
                time.sleep_ms(3000)
            print("Attempt", attempt, "done")
            time.sleep_ms(1000)
            attempt += 1
