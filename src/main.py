from wlan import connect_wlan, disconnect_wlan
from battery import Battery
from touchpad import Touchpad
from i2c import i2c_init, RealTimeClock
from spi import spi_init, tft_init
import rick

from machine import Pin
import machine
import webrepl
import time

import esp32
import _thread

import st7789
import vga2_bold_16x32
import vga2_8x16

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

TFT_ON = 0
TFT_OFF = 1

wlan = None
battery = Battery()
touchpad = Touchpad()
led = Pin(4, Pin.OUT)

spi = None
i2c = None

rtc = None
tft = None

last_time = (-1, -1)


def setup():
    global wlan, battery, touchpad, led, i2c, spi, rtc, tft
    wlan = None
    disconnect_wlan()
    battery = Battery()
    touchpad = Touchpad()
    led = Pin(4, Pin.OUT)
    i2c = i2c_init()
    spi = spi_init()
    rtc = RealTimeClock(i2c)
    tft = tft_init(spi)
    tft.init()
    tft.off()


def webrepl_start():
    global wlan
    wlan = connect_wlan()
    if wlan:
        webrepl.start(password='030218')


def webrepl_stop():
    global wlan
    webrepl.stop()
    disconnect_wlan()
    wlan = None


def deepsleep():
    global wlan, touchpad, i2c, spi, rtc, tft
    disconnect_wlan()
    tft.off()
    esp32.wake_on_ext0(pin=touchpad.touchpad, level=esp32.WAKEUP_ANY_HIGH)
    machine.deepsleep(1800000)


def on_long_press():
    global led, tft

    led.off()
    tft.off()
    webrepl_start()


def on_charge():
    global led

    led.on()
    return True


def on_uncharge():
    global led

    led.off()
    return False


def on_press(function, max_functions):
    global led, battery

    led.on()
    time.sleep_ms(200)
    led.off()
    if battery.is_charging():
        time.sleep_ms(100)
        led.on()
    return (function + 1) % max_functions


def draw_time():
    global tft, rtc, battery, last_time

    hours, minutes = rtc.hours(), rtc.minutes()

    if (hours, minutes) == last_time:
        return
    last_time = (hours, minutes)

    weekday = rtc.day() - 1
    volt = battery.voltage()

    tft.fill(st7789.BLACK)
    tft.text(vga2_bold_16x32, "%02d:%02d" % (hours, minutes), 0, 64, st7789.WHITE)
    tft.text(vga2_8x16, WEEKDAYS[weekday], 4, 96, st7789.GREEN if weekday < 5 else st7789.RED)

    tft.text(vga2_8x16, "%.2fV" % volt, 30, 126, st7789.GREEN if battery.is_charging() else st7789.WHITE)


def run_rickroll():
    global tft, touchpad, last_time

    channels = [10]
    tft.fill(st7789.BLACK)
    tft.text(vga2_bold_16x32, "R", 32, 16, st7789.WHITE)
    tft.text(vga2_bold_16x32, "i", 32, 48, st7789.WHITE) 
    tft.text(vga2_bold_16x32, "c", 32, 80, st7789.WHITE) 
    tft.text(vga2_bold_16x32, "k", 32, 112, st7789.WHITE) 
    rick.run(touchpad, channels)
    tft.fill(st7789.BLACK)
    last_time = (-1, -1)


def loop():
    global wlan, battery, touchpad, i2c, spi, rtc, tft

    max_functions = 2
    function = TFT_ON
    is_charging = not battery.is_charging()

    last_action = 0
    last_update = 0
    
    tft.on()

    while True:
        if battery.is_charging() and not is_charging:
            is_charging = on_charge()
            last_action = time.ticks_ms()
        elif not battery.is_charging and is_charging:
            is_charging = on_uncharge()
            last_action = time.ticks_ms()

        time_pressed = touchpad.check()
        if time_pressed > 2000 and function == TFT_OFF:
            on_long_press()
            break
        if time_pressed > 2000 and function == TFT_ON:
            run_rickroll()
            last_action = time.ticks_ms()
        if time_pressed:
            function = on_press(function, max_functions)
            if function == TFT_ON:
                tft.on()
            elif function == TFT_OFF:
                tft.off()
            last_action = time.ticks_ms()

        time_now = time.ticks_ms()

        if time.ticks_diff(time_now, last_update) > 1000 and function == TFT_ON:
            draw_time()
            last_update = time_now
        
        if time.ticks_diff(time_now, last_action) > 10000 and not battery.is_charging():
            function = TFT_OFF
            last_action = time_now
            deepsleep()


def main():
    setup()
    _thread.start_new_thread(loop, ())

main()