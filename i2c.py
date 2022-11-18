from machine import Pin, SoftI2C


PCF8563_SLAVE_ADDRESS = const(0x51)
PCF8563_SEC_REG = const(0x02)
PCF8563_MIN_REG = const(0x03)
PCF8563_HR_REG = const(0x04)
PCF8563_DAY_REG = const(0x05)
PCF8563_WEEKDAY_REG = const(0x06)
PCF8563_MONTH_REG = const(0x07)
PCF8563_YEAR_REG = const(0x08)


def i2c_init():
    return SoftI2C(scl=Pin(22, Pin.OUT), sda=Pin(21, Pin.OUT))


class RealTimeClock:
    def __init__(self, i2c):
        self.i2c = i2c
        self.buffer = bytearray(16)
        self.bytebuf = memoryview(self.buffer[0:1])

    def __read_byte(self, reg):
        self.i2c.readfrom_mem_into(PCF8563_SLAVE_ADDRESS, reg, self.bytebuf)
        return self.bytebuf[0]

    def __bcd2dec(self, bcd):
        return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

    def seconds(self):
        """Get the current allowed seconds of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_SEC_REG) & 0x7F)

    def minutes(self):
        """Get the current allowed minutes of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_MIN_REG) & 0x7F)

    def hours(self):
        """Get the current allowed hours of PCF8563
        """
        d = self.__read_byte(PCF8563_HR_REG) & 0x3F
        return self.__bcd2dec(d & 0x3F)

    def day(self):
        """Get the current allowed day of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_WEEKDAY_REG) & 0x07)

    def date(self):
        """Get the current allowed date of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_DAY_REG) & 0x3F)

    def month(self):
        """Get the current allowed month of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_MONTH_REG) & 0x1F)

    def year(self):
        """Get the current allowed year of PCF8563
        """
        return self.__bcd2dec(self.__read_byte(PCF8563_YEAR_REG))

    def datetime(self):
        """Return a tuple such as (year, month, date, day, hours, minutes,
        seconds).
        """
        return (self.year(), self.month(), self.date(),
                self.day(), self.hours(), self.minutes(),
                self.seconds())
