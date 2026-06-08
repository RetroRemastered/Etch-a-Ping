from machine import Pin, SoftSPI
import time


LCD_LED = 22
LCD_SCK = 18
LCD_MOSI = 19
LCD_DC = 20
LCD_RST = 21
LCD_CS = 17

WIDTH = 160
HEIGHT = 128

COLORS = (0xF800, 0x07E0, 0x001F, 0x0000)


def blink_backlight():
    led = Pin(LCD_LED, Pin.OUT)
    for _ in range(6):
        led(0)
        time.sleep_ms(250)
        led(1)
        time.sleep_ms(250)


class ST7735Probe:
    def __init__(self, sck_pin, mosi_pin):
        self.spi = SoftSPI(
            baudrate=500_000,
            polarity=0,
            phase=0,
            sck=Pin(sck_pin),
            mosi=Pin(mosi_pin),
            miso=Pin(16),
        )
        self.dc = Pin(LCD_DC, Pin.OUT, value=0)
        self.cs = Pin(LCD_CS, Pin.OUT, value=1)
        self.rst = Pin(LCD_RST, Pin.OUT, value=1)

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
        time.sleep_ms(100)
        self.rst(1)
        time.sleep_ms(250)

        self.cmd(0x01)
        time.sleep_ms(250)
        self.cmd(0x11)
        time.sleep_ms(250)
        self.cmd(0x3A, b"\x05")
        self.cmd(0x36, b"\x60")
        self.cmd(0x29)
        time.sleep_ms(250)

    def window(self):
        self.cmd(0x2A, bytes([0, 0, 0, WIDTH - 1]))
        self.cmd(0x2B, bytes([0, 0, 0, HEIGHT - 1]))
        self.cmd(0x2C)

    def fill(self, color):
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo]) * WIDTH
        self.window()
        self.cs(0)
        self.dc(1)
        for _ in range(HEIGHT):
            self.spi.write(row)
        self.cs(1)


blink_backlight()

while True:
    # First try the pinout as soldered: CLK GP18, SDI GP19.
    lcd = ST7735Probe(18, 19)
    lcd.init()
    for color in COLORS:
        lcd.fill(color)
        time.sleep_ms(700)

    # Then try the common accidental swap: CLK GP19, SDI GP18.
    lcd = ST7735Probe(19, 18)
    lcd.init()
    for color in COLORS:
        lcd.fill(color)
        time.sleep_ms(700)
