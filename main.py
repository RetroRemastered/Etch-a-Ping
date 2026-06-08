from machine import ADC, Pin, SPI
from rp2 import PIO, StateMachine, asm_pio
import random
import time


# ILI9225 red breakout screen pins, matching your soldered wiring.
LCD_LED = 22
LCD_SCK = 18   # Screen CLK
LCD_MOSI = 19  # Screen SDI
LCD_RS = 20
LCD_RST = 21
LCD_CS = 17

# Two potentiometers. Outer legs go to 3V3 and GND; center wipers go here.
POT_LEFT = 26   # ADC0
POT_RIGHT = 27  # ADC1

# MAX98357A I2S amp pins. These are digital pins so the ADC pins stay free.
I2S_LRC = 10
I2S_BCLK = 11
I2S_DIN = 12
START_BUTTON = 13
AUDIO_RATE = 16_000
AUDIO_VOLUME = 2250
PADDLE_SENSITIVITY = 4

PHYS_WIDTH = 176
PHYS_HEIGHT = 220
WIDTH = 220
HEIGHT = 176
PLAY_LEFT = 0
PLAY_RIGHT = WIDTH

BLACK = 0x0000
WHITE = 0xFFFF
BACKGROUND = 0x8410
FOREGROUND = BLACK
BALL_SPEED = 4
SERVE_SPEED = 3

DIGITS = {
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
}

LETTERS = {
    "G": ("01110", "10000", "10000", "10111", "10001", "10001", "01110"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
}


class ILI9225:
    def __init__(self):
        self.spi = SPI(
            0,
            baudrate=16_000_000,
            polarity=0,
            phase=0,
            sck=Pin(LCD_SCK),
            mosi=Pin(LCD_MOSI),
        )
        self.led = Pin(LCD_LED, Pin.OUT, value=1)
        self.rs = Pin(LCD_RS, Pin.OUT, value=0)
        self.cs = Pin(LCD_CS, Pin.OUT, value=1)
        self.rst = Pin(LCD_RST, Pin.OUT, value=1)
        self.init()

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
        self.fill(BACKGROUND)

    def orient(self, x, y):
        return y, PHYS_HEIGHT - x - 1

    def set_window(self, x0, y0, x1, y1):
        x0, y0 = self.orient(x0, y0)
        x1, y1 = self.orient(x1, y1)
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0

        self.write_register(0x36, x1)
        self.write_register(0x37, x0)
        self.write_register(0x38, y1)
        self.write_register(0x39, y0)
        self.write_register(0x20, x0)
        self.write_register(0x21, y0)
        self.write_command(0x0022)

    def fill_rect(self, x, y, w, h, color):
        if w <= 0 or h <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(WIDTH - 1, x + w - 1)
        y1 = min(HEIGHT - 1, y + h - 1)
        if x0 > x1 or y0 > y1:
            return

        hi = color >> 8
        lo = color & 0xFF
        pixel = bytes([hi, lo])
        count = (x1 - x0 + 1) * (y1 - y0 + 1)
        chunk = pixel * min(count, 256)

        self.set_window(x0, y0, x1, y1)
        self.cs(0)
        self.rs(1)
        while count:
            n = min(count, 256)
            self.spi.write(chunk[: n * 2])
            count -= n
        self.cs(1)

    def fill(self, color):
        self.fill_rect(0, 0, WIDTH, HEIGHT, color)

    def blit_rgb565(self, x, y, w, h, buffer):
        if w <= 0 or h <= 0:
            return
        self.set_window(x, y, x + w - 1, y + h - 1)
        self.cs(0)
        self.rs(1)
        self.spi.write(buffer)
        self.cs(1)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def pot_to_y(adc, paddle_h):
    raw = adc.read_u16()
    raw = clamp((raw - 32768) * PADDLE_SENSITIVITY + 32768, 0, 65535)
    return -paddle_h // 2 + (raw * HEIGHT) // 65535


def auto_y(ball_y, paddle_h):
    return clamp(ball_y - paddle_h // 2, -paddle_h // 2, HEIGHT - paddle_h // 2)


def reset_ball(direction=None):
    dx = direction if direction else random.choice((-SERVE_SPEED, SERVE_SPEED))
    dy = random.choice((-3, -2, 2, 3))
    return (PLAY_LEFT + PLAY_RIGHT) // 2, HEIGHT // 2, dx, dy


def has_winner(score_l, score_r):
    if score_l >= 11 and score_l - score_r >= 2:
        return 1
    if score_r >= 11 and score_r - score_l >= 2:
        return 2
    return 0


def draw_digit_to_buffer(buffer, area_w, digit, x, y, scale, color):
    rows = DIGITS[str(digit)]
    hi = color >> 8
    lo = color & 0xFF
    for row_i, row in enumerate(rows):
        for col_i, pixel in enumerate(row):
            if pixel != "1":
                continue
            px = x + col_i * scale
            py = y + row_i * scale
            for yy in range(py, py + scale):
                for xx in range(px, px + scale):
                    offset = (yy * area_w + xx) * 2
                    buffer[offset] = hi
                    buffer[offset + 1] = lo


def draw_number_to_buffer(buffer, area_w, value, x, y, scale, color):
    text = str(value)
    digit_w = 3 * scale
    gap = scale
    for i, digit in enumerate(text):
        draw_digit_to_buffer(buffer, area_w, digit, x + i * (digit_w + gap), y, scale, color)


def draw_digit(lcd, digit, x, y, scale, color):
    rows = DIGITS[str(digit)]
    for row_i, row in enumerate(rows):
        for col_i, pixel in enumerate(row):
            if pixel == "1":
                lcd.fill_rect(
                    x + col_i * scale,
                    y + row_i * scale,
                    scale,
                    scale,
                    color,
                )


def draw_number(lcd, value, x, y, scale, color):
    text = str(value)
    digit_w = 3 * scale
    gap = scale
    for i, digit in enumerate(text):
        draw_digit(lcd, digit, x + i * (digit_w + gap), y, scale, color)


def number_width(value, scale):
    return len(str(value)) * 3 * scale + max(0, len(str(value)) - 1) * scale


def draw_letter(lcd, letter, x, y, scale, color):
    rows = LETTERS[letter]
    for row_i, row in enumerate(rows):
        for col_i, pixel in enumerate(row):
            if pixel == "1":
                lcd.fill_rect(
                    x + col_i * scale,
                    y + row_i * scale,
                    scale,
                    scale,
                    color,
                )


def draw_text(lcd, text, x, y, scale, color):
    letter_w = 5 * scale
    gap = scale
    for i, letter in enumerate(text):
        draw_letter(lcd, letter, x + i * (letter_w + gap), y, scale, color)


def text_width(text, scale):
    return len(text) * 5 * scale + max(0, len(text) - 1) * scale


def wait_for_start(lcd, button):
    lcd.fill(BACKGROUND)
    scale = 8
    title = "PING"
    x = (WIDTH - text_width(title, scale)) // 2
    y = (HEIGHT - 7 * scale) // 2
    draw_text(lcd, title, x, y, scale, FOREGROUND)

    while button.value() == 0:
        time.sleep_ms(20)
    while button.value() == 1:
        time.sleep_ms(20)
    time.sleep_ms(80)
    while button.value() == 0:
        time.sleep_ms(20)

    lcd.fill(BACKGROUND)
    time.sleep_ms(650)


def wait_for_button_press(button):
    while button.value() == 0:
        time.sleep_ms(20)
    while button.value() == 1:
        time.sleep_ms(20)
    time.sleep_ms(80)
    while button.value() == 0:
        time.sleep_ms(20)


def draw_scoreboard(lcd, score_l, score_r):
    lcd.fill_rect(64, 5, 92, 18, BACKGROUND)
    scale = 3
    left_w = number_width(score_l, scale)
    draw_number(lcd, score_l, WIDTH // 2 - 18 - left_w, 6, scale, FOREGROUND)
    draw_number(lcd, score_r, WIDTH // 2 + 18, 6, scale, FOREGROUND)


def clear_scoreboard(lcd):
    lcd.fill_rect(64, 5, 92, 18, BACKGROUND)


def wait_with_score(
    lcd,
    left_pot,
    right_pot,
    left_x,
    right_x,
    paddle_w,
    paddle_h,
    score_l,
    score_r,
    last_left_y,
    last_right_y,
):
    end_at = time.ticks_add(time.ticks_ms(), 900)
    while time.ticks_diff(end_at, time.ticks_ms()) > 0:
        left_y = pot_to_y(left_pot, paddle_h) if left_pot else HEIGHT // 2 - paddle_h // 2
        right_y = pot_to_y(right_pot, paddle_h) if right_pot else HEIGHT // 2 - paddle_h // 2
        draw_paddle_during_pause(lcd, left_x, last_left_y, left_y, paddle_w, paddle_h)
        draw_paddle_during_pause(lcd, right_x, last_right_y, right_y, paddle_w, paddle_h)
        last_left_y = left_y
        last_right_y = right_y
        time.sleep_ms(12)
    return last_left_y, last_right_y


def show_winner(lcd, score_l, score_r, winner):
    lcd.fill(BACKGROUND)
    scale = 7
    left_w = number_width(score_l, scale)
    right_w = number_width(score_r, scale)
    left_x = (WIDTH // 4) - (left_w // 2)
    right_x = (WIDTH * 3 // 4) - (right_w // 2)
    y = HEIGHT // 2 - 18
    draw_number(lcd, score_l, left_x, y, scale, FOREGROUND)
    draw_number(lcd, score_r, right_x, y, scale, FOREGROUND)
    if winner == 1:
        lcd.fill_rect(left_x, y + 42, left_w, 4, FOREGROUND)
    else:
        lcd.fill_rect(right_x, y + 42, right_w, 4, FOREGROUND)


def paddle_deflection(ball_y, ball_size, paddle_y, paddle_h):
    ball_center = ball_y + ball_size // 2
    paddle_center = paddle_y + paddle_h // 2
    offset = ball_center - paddle_center
    max_offset = max(1, paddle_h // 2)
    return clamp((offset * 4) // max_offset, -4, 4)


def rects_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def ball_touched_paddle_area(ball_x, ball_y, ball_size, paddle_x, old_y, new_y, paddle_w, paddle_h):
    if old_y != -1 and rects_overlap(
        ball_x, ball_y, ball_size, ball_size, paddle_x, old_y, paddle_w, paddle_h
    ):
        return True
    return rects_overlap(
        ball_x, ball_y, ball_size, ball_size, paddle_x, new_y, paddle_w, paddle_h
    )


def draw_paddle(lcd, x, old_y, new_y, w, h, force=False):
    if old_y == -1 or force:
        if old_y != -1:
            lcd.fill_rect(x, old_y, w, h, BACKGROUND)
        lcd.fill_rect(x, new_y, w, h, FOREGROUND)
        return

    if new_y == old_y:
        return

    old_top = max(0, old_y)
    old_bottom = min(HEIGHT, old_y + h)
    new_top = max(0, new_y)
    new_bottom = min(HEIGHT, new_y + h)

    if old_top < old_bottom:
        if old_top < new_top:
            lcd.fill_rect(x, old_top, w, min(old_bottom, new_top) - old_top, BACKGROUND)
        if old_bottom > new_bottom:
            lcd.fill_rect(x, max(old_top, new_bottom), w, old_bottom - max(old_top, new_bottom), BACKGROUND)

    if new_top < new_bottom:
        if new_top < old_top:
            lcd.fill_rect(x, new_top, w, min(new_bottom, old_top) - new_top, FOREGROUND)
        if new_bottom > old_bottom:
            lcd.fill_rect(x, max(new_top, old_bottom), w, new_bottom - max(new_top, old_bottom), FOREGROUND)


def draw_paddle_during_pause(lcd, x, old_y, new_y, w, h):
    if old_y < 0 or old_y + h > HEIGHT or new_y < 0 or new_y + h > HEIGHT:
        lcd.fill_rect(x, 0, w, HEIGHT, BACKGROUND)
        lcd.fill_rect(x, new_y, w, h, FOREGROUND)
    else:
        draw_paddle(lcd, x, old_y, new_y, w, h)


@asm_pio(
    out_init=PIO.OUT_LOW,
    set_init=PIO.OUT_LOW,
    out_shiftdir=PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=32,
    sideset_init=PIO.OUT_LOW,
)
def i2s_square_wave_out():
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


class Beeper:
    def __init__(self):
        self.audio = StateMachine(
            0,
            i2s_square_wave_out,
            freq=AUDIO_RATE * 32 * 3,
            out_base=Pin(I2S_DIN),
            set_base=Pin(I2S_LRC),
            sideset_base=Pin(I2S_BCLK),
        )
        self.audio.active(1)

    def beep(self, freq, duration_ms=35):
        sample_count = max(1, (AUDIO_RATE * duration_ms) // 1000)
        period = max(2, AUDIO_RATE // freq)
        half_period = period // 2

        for i in range(sample_count):
            sample = AUDIO_VOLUME if i % period < half_period else -AUDIO_VOLUME
            if sample < 0:
                sample += 65536
            self.audio.put((sample << 16) | sample)

    def update(self):
        pass

    def score(self):
        self.beep(60, 20)


def update_paddles_once(lcd, left_pot, right_pot, left_x, right_x, paddle_w, paddle_h, last_left_y, last_right_y):
    left_y = pot_to_y(left_pot, paddle_h) if left_pot else HEIGHT // 2 - paddle_h // 2
    right_y = pot_to_y(right_pot, paddle_h) if right_pot else HEIGHT // 2 - paddle_h // 2
    draw_paddle_during_pause(lcd, left_x, last_left_y, left_y, paddle_w, paddle_h)
    draw_paddle_during_pause(lcd, right_x, last_right_y, right_y, paddle_w, paddle_h)
    return left_y, right_y


def main():
    lcd = ILI9225()
    left_pot = ADC(POT_LEFT) if POT_LEFT is not None else None
    right_pot = ADC(POT_RIGHT) if POT_RIGHT is not None else None
    start_button = Pin(START_BUTTON, Pin.IN, Pin.PULL_UP)
    beeper = Beeper()
    wait_for_start(lcd, start_button)

    paddle_w = 5
    paddle_h = 34
    ball_size = 5
    left_x = PLAY_LEFT + 8
    right_x = PLAY_RIGHT - 13
    score_l = 0
    score_r = 0
    ball_x, ball_y, ball_dx, ball_dy = reset_ball()

    last_left_y = last_right_y = -1
    last_ball_x = last_ball_y = -1

    lcd.fill(BACKGROUND)

    while True:
        beeper.update()

        left_y = pot_to_y(left_pot, paddle_h) if left_pot else auto_y(ball_y, paddle_h)
        right_y = pot_to_y(right_pot, paddle_h) if right_pot else auto_y(ball_y, paddle_h)

        next_x = ball_x + ball_dx
        next_y = ball_y + ball_dy

        if next_y <= 0 or next_y >= HEIGHT - ball_size:
            ball_dy = -ball_dy
            next_y = ball_y + ball_dy
            beeper.beep(500, 35)

        left_hit = (
            next_x <= left_x + paddle_w
            and next_x + ball_size >= left_x
            and next_y + ball_size >= left_y
            and next_y <= left_y + paddle_h
        )
        right_hit = (
            next_x + ball_size >= right_x
            and next_x <= right_x + paddle_w
            and next_y + ball_size >= right_y
            and next_y <= right_y + paddle_h
        )

        if left_hit:
            ball_dx = BALL_SPEED
            ball_dy = paddle_deflection(next_y, ball_size, left_y, paddle_h)
            next_x = left_x + paddle_w + 1
            beeper.beep(1000, 35)
        elif right_hit:
            ball_dx = -BALL_SPEED
            ball_dy = paddle_deflection(next_y, ball_size, right_y, paddle_h)
            next_x = right_x - ball_size - 1
            beeper.beep(1000, 35)

        if next_x < PLAY_LEFT:
            score_r += 1
            beeper.score()
            winner = has_winner(score_l, score_r)
            if winner:
                show_winner(lcd, score_l, score_r, winner)
                wait_for_button_press(start_button)
                score_l = 0
                score_r = 0
                lcd.fill(BACKGROUND)
                time.sleep_ms(650)
                last_left_y = last_right_y = -1
                last_ball_x = last_ball_y = -1
                ball_x, ball_y, ball_dx, ball_dy = reset_ball(-SERVE_SPEED)
                continue
            lcd.fill_rect(ball_x, ball_y, ball_size, ball_size, BACKGROUND)
            last_left_y, last_right_y = update_paddles_once(
                lcd, left_pot, right_pot, left_x, right_x, paddle_w, paddle_h, last_left_y, last_right_y
            )
            draw_scoreboard(lcd, score_l, score_r)
            last_left_y, last_right_y = wait_with_score(
                lcd,
                left_pot,
                right_pot,
                left_x,
                right_x,
                paddle_w,
                paddle_h,
                score_l,
                score_r,
                last_left_y,
                last_right_y,
            )
            clear_scoreboard(lcd)
            last_left_y, last_right_y = update_paddles_once(
                lcd, left_pot, right_pot, left_x, right_x, paddle_w, paddle_h, last_left_y, last_right_y
            )
            ball_x, ball_y, ball_dx, ball_dy = reset_ball(-SERVE_SPEED)
            last_ball_x = last_ball_y = -1
            beeper.update()
            continue
        if next_x > PLAY_RIGHT - ball_size:
            score_l += 1
            beeper.score()
            winner = has_winner(score_l, score_r)
            if winner:
                show_winner(lcd, score_l, score_r, winner)
                wait_for_button_press(start_button)
                score_l = 0
                score_r = 0
                lcd.fill(BACKGROUND)
                time.sleep_ms(650)
                last_left_y = last_right_y = -1
                last_ball_x = last_ball_y = -1
                ball_x, ball_y, ball_dx, ball_dy = reset_ball(SERVE_SPEED)
                continue
            lcd.fill_rect(ball_x, ball_y, ball_size, ball_size, BACKGROUND)
            last_left_y, last_right_y = update_paddles_once(
                lcd, left_pot, right_pot, left_x, right_x, paddle_w, paddle_h, last_left_y, last_right_y
            )
            draw_scoreboard(lcd, score_l, score_r)
            last_left_y, last_right_y = wait_with_score(
                lcd,
                left_pot,
                right_pot,
                left_x,
                right_x,
                paddle_w,
                paddle_h,
                score_l,
                score_r,
                last_left_y,
                last_right_y,
            )
            clear_scoreboard(lcd)
            last_left_y, last_right_y = update_paddles_once(
                lcd, left_pot, right_pot, left_x, right_x, paddle_w, paddle_h, last_left_y, last_right_y
            )
            ball_x, ball_y, ball_dx, ball_dy = reset_ball(SERVE_SPEED)
            last_ball_x = last_ball_y = -1
            beeper.update()
            continue

        if last_ball_x != -1:
            lcd.fill_rect(last_ball_x, last_ball_y, ball_size, ball_size, BACKGROUND)

        ball_x, ball_y = next_x, next_y

        redraw_left = last_ball_x != -1 and ball_touched_paddle_area(
            last_ball_x, last_ball_y, ball_size, left_x, last_left_y, left_y, paddle_w, paddle_h
        )
        redraw_right = last_ball_x != -1 and ball_touched_paddle_area(
            last_ball_x, last_ball_y, ball_size, right_x, last_right_y, right_y, paddle_w, paddle_h
        )

        draw_paddle(lcd, left_x, last_left_y, left_y, paddle_w, paddle_h, redraw_left)
        draw_paddle(lcd, right_x, last_right_y, right_y, paddle_w, paddle_h, redraw_right)
        lcd.fill_rect(ball_x, ball_y, ball_size, ball_size, FOREGROUND)

        last_left_y = left_y
        last_right_y = right_y
        last_ball_x = ball_x
        last_ball_y = ball_y

        time.sleep_ms(12)


main()
