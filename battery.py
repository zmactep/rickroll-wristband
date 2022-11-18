from machine import ADC, Pin


class Battery:
    def __init__(self):
        self.battery_pin = ADC(Pin(35, Pin.IN))
        self.battery_pin.width(ADC.WIDTH_9BIT)
        self.battery_pin.atten(ADC.ATTN_11DB)

        self.charge_pin = Pin(32, Pin.IN, Pin.PULL_UP)

        self.vbus_pin = ADC(Pin(36, Pin.IN))
        self.vbus_pin.width(ADC.WIDTH_9BIT)
        self.vbus_pin.atten(ADC.ATTN_11DB)

    def voltage(self):
        return (self.battery_pin.read() + 6) / 100.0

    def is_charging(self):
        return self.charge_pin.value() == 0

    def vbus_voltage(self):
        return self.vbus_pin.read() / 100.0

    def status(self):
        val = self.voltage()
        if val > 2.66:
            return 'high'
        elif val > 2.36:
            return 'medium'
        elif val > 2.16:
            return 'low'
        return 'critical'
