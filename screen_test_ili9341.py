from machine import Pin, SoftSPI
import time


LCD_LED = 22
LCD_SCK = 18
LCD_MOSI = 19
LCD_DC = 20
LCD_RST = 21
LCD_CS = 17

WIDTH = 320
HEIGHT = 240

COLORS = (
    ("RED", 0xF800),
    ("GREEN", 0x07E0),
    ("BLUE", 0x001F),
    ("YELLOW", 0xFFE0),
    ("MAGENTA", 0xF81F),
    ("CYAN", 0x07FF),
    ("BLACK", 0x0000),
)


class ILI9341Test:
    def __init__(self):
        self.spi = SoftSPI(
            baudrate=2_000_000,
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
        time.sleep_ms(250)

    def init(self):
        self.reset()
        self.cmd(0x01)
        time.sleep_ms(200)
        self.cmd(0x28)
        self.cmd(0xCF, b"\x00\xC1\x30")
        self.cmd(0xED, b"\x64\x03\x12\x81")
        self.cmd(0xE8, b"\x85\x00\x78")
        self.cmd(0xCB, b"\x39\x2C\x00\x34\x02")
        self.cmd(0xF7, b"\x20")
        self.cmd(0xEA, b"\x00\x00")
        self.cmd(0xC0, b"\x23")
        self.cmd(0xC1, b"\x10")
        self.cmd(0xC5, b"\x3E\x28")
        self.cmd(0xC7, b"\x86")
        self.cmd(0x36, b"\x28")
        self.cmd(0x3A, b"\x55")
        self.cmd(0xB1, b"\x00\x18")
        self.cmd(0xB6, b"\x08\x82\x27")
        self.cmd(0xF2, b"\x00")
        self.cmd(0x26, b"\x01")
        self.cmd(
            0xE0,
            b"\x0F\x31\x2B\x0C\x0E\x08\x4E\xF1\x37\x07\x10\x03\x0E\x09\x00",
        )
        self.cmd(
            0xE1,
            b"\x00\x0E\x14\x03\x11\x07\x31\xC1\x48\x08\x0F\x0C\x31\x36\x0F",
        )
        self.cmd(0x11)
        time.sleep_ms(150)
        self.cmd(0x29)
        time.sleep_ms(150)

    def set_window(self, x0, y0, x1, y1):
        self.cmd(
            0x2A,
            bytes([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]),
        )
        self.cmd(
            0x2B,
            bytes([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]),
        )
        self.cmd(0x2C)

    def fill(self, color):
        hi = color >> 8
        lo = color & 0xFF
        row = bytes([hi, lo]) * WIDTH
        self.set_window(0, 0, WIDTH - 1, HEIGHT - 1)
        self.cs(0)
        self.dc(1)
        for _ in range(HEIGHT):
            self.spi.write(row)
        self.cs(1)


lcd = ILI9341Test()
lcd.init()

while True:
    for name, color in COLORS:
        print("Drawing", name)
        lcd.fill(color)
        time.sleep(1)
