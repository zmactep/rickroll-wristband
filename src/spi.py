from machine import Pin, SPI
import st7789

SCK_PIN = 18
MOSI_PIN = 19
MISO_PIN = 23
CS_PIN = 5
DC_PIN = 23
RST_PIN = 26
BL_PIN = 27

def spi_init():
    return SPI(2, sck = Pin(SCK_PIN, Pin.OUT),
               mosi = Pin(MOSI_PIN, Pin.OUT), miso = Pin(MISO_PIN, Pin.OUT),
               baudrate = 30000000, polarity = 0, phase = 0)

def tft_init(spi):
    return st7789.ST7789(spi, 80, 160,
                         reset = Pin(RST_PIN, Pin.OUT),
                         cs = Pin(CS_PIN, Pin.OUT),
                         dc = Pin(DC_PIN, Pin.OUT),
                         backlight = Pin(BL_PIN, Pin.OUT),
                         color_order = st7789.BGR,
                         inversion = False,
                         rotation = 2)
