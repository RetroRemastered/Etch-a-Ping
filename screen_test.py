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

BLACK = 0x0000
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
WHITE = 0xFFFF


class ST7735Test:
    def __init__(self):
        self.spi = SoftSPI(
            baudrate=1_000_000,
            polarity=0,
            phase=0,
            sck=Pin(LCD_SCK),
            mosi=Pin(LCD_MOSI),
            miso=Pin(16),
        )
        self.led = Pin(LCD_LED, Pin.OUT, value=1)
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

    def reset(self):
        self.cs(1)
        self.rst(1)
        time.sleep_ms(100)
        self.rst(0)
        time.sleep_ms(100)
        self.rst(1)
        time.sleep_ms(200)

    def init(self):
        self.reset()
        self.cmd(0x01)
        time.sleep_ms(200)
        self.cmd(0x11)
        time.sleep_ms(200)
        self.cmd(0x3A, b"\x05")
        self.cmd(0x36, b"\x60")
        self.cmd(0xB1, b"\x01\x2C\x2D")
        self.cmd(0xB2, b"\x01\x2C\x2D")
        self.cmd(0xB3, b"\x01\x2C\x2D\x01\x2C\x2D")
        self.cmd(0xB4, b"\x07")
        self.cmd(0xC0, b"\xA2\x02\x84")
        self.cmd(0xC1, b"\xC5")
        self.cmd(0xC2, b"\x0A\x00")
        self.cmd(0xC3, b"\x8A\x2A")
        self.cmd(0xC4, b"\x8A\xEE")
        self.cmd(0xC5, b"\x0E")
        self.cmd(0x13)
        self.cmd(0x29)
        time.sleep_ms(200)

    def window(self, x0, y0, x1, y1):
        self.cmd(0x2A, bytes([0, x0, 0, x1]))
        self.cmd(0x2B, bytes([0, y0, 0, y1]))
        self.cmd(0x2C)

    def fill(self, color):
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo]) * WIDTH
        self.window(0, 0, WIDTH - 1, HEIGHT - 1)
        self.cs(0)
        self.dc(1)
        for _ in range(HEIGHT):
            self.spi.write(row)
        self.cs(1)


lcd = ST7735Test()
lcd.init()

while True:
    lcd.fill(RED)
    time.sleep(1)
    lcd.fill(GREEN)
    time.sleep(1)
    lcd.fill(BLUE)
    time.sleep(1)
    lcd.fill(WHITE)
    time.sleep(1)
    lcd.fill(BLACK)
    time.sleep(1)
