from machine import Pin, SoftSPI
import time


LCD_LED = 22
LCD_SCK = 18
LCD_MOSI = 19
LCD_DC = 20
LCD_RST = 21
LCD_CS = 17


spi = SoftSPI(
    baudrate=100_000,
    polarity=0,
    phase=0,
    sck=Pin(LCD_SCK),
    mosi=Pin(LCD_MOSI),
    miso=Pin(16),
)
led = Pin(LCD_LED, Pin.OUT, value=1)
dc = Pin(LCD_DC, Pin.OUT, value=0)
cs = Pin(LCD_CS, Pin.OUT, value=1)
rst = Pin(LCD_RST, Pin.OUT, value=1)


def cmd(value, data=None):
    cs(0)
    dc(0)
    spi.write(bytes([value]))
    if data:
        dc(1)
        spi.write(data)
    cs(1)


def hard_reset():
    print("hardware reset")
    rst(1)
    time.sleep_ms(300)
    rst(0)
    time.sleep_ms(500)
    rst(1)
    time.sleep_ms(500)


hard_reset()

while True:
    print("software reset")
    cmd(0x01)
    time.sleep(1)

    print("sleep out")
    cmd(0x11)
    time.sleep(1)

    print("display off")
    cmd(0x28)
    time.sleep(2)

    print("display on")
    cmd(0x29)
    time.sleep(2)

    print("invert on")
    cmd(0x21)
    time.sleep(2)

    print("invert off")
    cmd(0x20)
    time.sleep(2)
