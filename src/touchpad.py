from machine import Pin
import time

TP_PIN_PIN = 33
TP_PWR_PIN = 25


class Touchpad:
    def __init__(self):
        self.touchpad = Pin(TP_PIN_PIN, Pin.IN, hold=True)
        self.touchpad_power = Pin(TP_PWR_PIN, Pin.PULL_UP, value=1, hold=True)

    def check(self):
        if self.touchpad.value():
            if self.is_pressed:
                self.press_time = time.ticks_diff(time.ticks_ms(), self.press_start)
            else:
                self.is_pressed = True
                self.press_start = time.ticks_ms()
                self.press_time = 0
        else:
            self.is_pressed = False

    def check(self):
        if self.touchpad.value():
            start_time = time.ticks_ms()
            while self.touchpad.value():
                time.sleep_ms(10)
            return time.ticks_diff(time.ticks_ms(), start_time)
        return 0
