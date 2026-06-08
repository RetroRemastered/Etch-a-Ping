from machine import Pin, SoftSPI
import time


LCD_LED = 22
LCD_SCK = 18
LCD_MOSI = 19
LCD_RS = 20
LCD_RST = 21
LCD_CS = 17

WIDTH = 176
HEIGHT = 220

COLORS = (
    ("RED", 0xF800),
    ("GREEN", 0x07E0),
    ("BLUE", 0x001F),
    ("YELLOW", 0xFFE0),
    ("MAGENTA", 0xF81F),
    ("CYAN", 0x07FF),
    ("BLACK", 0x0000),
)


class ILI9225:
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
        self.rs = Pin(LCD_RS, Pin.OUT, value=0)
        self.cs = Pin(LCD_CS, Pin.OUT, value=1)
        self.rst = Pin(LCD_RST, Pin.OUT, value=1)

    def write_command(self, value):
        self.rs(0)
        self.cs(0)
        self.spi.write(bytes([(value >> 8) & 0xFF, value & 0xFF]))
        self.cs(1)

    def write_data(self, value):
        self.rs(1)
        self.cs(0)
        self.spi.write(bytes([(value >> 8) & 0xFF, value & 0xFF]))
        self.cs(1)

    def write_register(self, reg, value):
        self.write_command(reg)
        self.write_data(value)

    def reset(self):
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(20)
        self.rst(1)
        time.sleep_ms(80)

    def init(self):
        self.reset()

        self.write_register(0x10, 0x0000)
        self.write_register(0x11, 0x0000)
        self.write_register(0x12, 0x0000)
        self.write_register(0x13, 0x0000)
        self.write_register(0x14, 0x0000)
        time.sleep_ms(40)

        self.write_register(0x11, 0x0018)
        self.write_register(0x12, 0x6121)
        self.write_register(0x13, 0x006F)
        self.write_register(0x14, 0x495F)
        self.write_register(0x10, 0x0800)
        time.sleep_ms(10)
        self.write_register(0x11, 0x103B)
        time.sleep_ms(50)

        self.write_register(0x01, 0x011C)
        self.write_register(0x02, 0x0100)
        self.write_register(0x03, 0x1030)
        self.write_register(0x07, 0x0000)
        self.write_register(0x08, 0x0808)
        self.write_register(0x0B, 0x1100)
        self.write_register(0x0C, 0x0000)
        self.write_register(0x0F, 0x0D01)
        self.write_register(0x15, 0x0020)
        self.write_register(0x20, 0x0000)
        self.write_register(0x21, 0x0000)

        self.write_register(0x30, 0x0000)
        self.write_register(0x31, 0x00DB)
        self.write_register(0x32, 0x0000)
        self.write_register(0x33, 0x0000)
        self.write_register(0x34, 0x00DB)
        self.write_register(0x35, 0x0000)
        self.write_register(0x36, 0x00AF)
        self.write_register(0x37, 0x0000)
        self.write_register(0x38, 0x00DB)
        self.write_register(0x39, 0x0000)

        self.write_register(0x50, 0x0000)
        self.write_register(0x51, 0x0808)
        self.write_register(0x52, 0x080A)
        self.write_register(0x53, 0x000A)
        self.write_register(0x54, 0x0A08)
        self.write_register(0x55, 0x0808)
        self.write_register(0x56, 0x0000)
        self.write_register(0x57, 0x0A00)
        self.write_register(0x58, 0x0710)
        self.write_register(0x59, 0x0710)

        self.write_register(0x07, 0x0012)
        time.sleep_ms(50)
        self.write_register(0x07, 0x1017)
        time.sleep_ms(100)

    def set_window(self, x0, y0, x1, y1):
        self.write_register(0x36, x1)
        self.write_register(0x37, x0)
        self.write_register(0x38, y1)
        self.write_register(0x39, y0)
        self.write_register(0x20, x0)
        self.write_register(0x21, y0)
        self.write_command(0x0022)

    def fill(self, color):
        row = bytes([(color >> 8) & 0xFF, color & 0xFF]) * WIDTH
        self.set_window(0, 0, WIDTH - 1, HEIGHT - 1)
        self.rs(1)
        self.cs(0)
        for _ in range(HEIGHT):
            self.spi.write(row)
        self.cs(1)


lcd = ILI9225()
lcd.init()

while True:
    for name, color in COLORS:
        print("Drawing", name)
        lcd.fill(color)
        time.sleep(1)
