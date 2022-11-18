import network
import time
from urandom import getrandbits

PACKET = [
    0x80, 0x00, 0x00, 0x00,                                 #  0 - 3  : Type, Subtype (Beacon Frame)
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff,                     #  4 - 9  : Destionation Address (broadcast)
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                     # 10 - 15 : Source Address
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                     # 16 - 21 : Source Address
    0x00, 0x00,                                             # 22 - 23 : Sequence Control
    0x83, 0x51, 0xf7, 0x8f, 0x0f, 0x00, 0x00, 0x00,         # 24 - 31 : Timestamp
    0xe8, 0x03,                                             # 32 - 33 : Interval (0x64, 0x00 : 100ms, 0xe8, 0x03 : 1s)
    0x31, 0x00,                                             # 34 - 35 : Capability Info
    0x00, 0x20                                              # 36 - 37 : ESSID Length
]

TAIL = [
    # Supported rates
    0x01, 0x08,
    0x82, 0x84, 0x8b, 0x96,
    0x24, 0x30, 0x48, 0x6c,

    # Channel
    0x03, 0x01,
    0x01,

    # RSN information
    0x30, 0x18,
    0x01, 0x00,
    0x00, 0x0f, 0xac, 0x02,
    0x02, 0x00,
    0x00, 0x0f, 0xac, 0x04, 0x00, 0x0f, 0xac, 0x04,
    0x01, 0x00,
    0x00, 0x0f, 0xac, 0x02,
    0x00, 0x00
]

RICK_SSIDS = [
    "01 Never gonna give you up",
	"02 Never gonna let you down",
	"03 Never gonna run around",
	"04 and desert you",
	"05 Never gonna make you cry",
	"06 Never gonna say goodbye",
	"07 Never gonna tell a lie",
	"08 and hurt you"
]


class TimeExit:
    def __init__(self, timeout):
        self.start = time.ticks_ms()
        self.timeout = timeout

    def check(self):
        if time.ticks_diff(time.ticks_ms(), self.start) > self.timeout:
            return True


def make_packet(ssid, channel):
    packet = bytearray(PACKET)
    tail = bytearray(TAIL)
    ssid = bytes(ssid, "utf8")

    # Generate random BSSID and MAC
    for i in range(6):
        packet[10 + i] = packet[16 + i] = getrandbits(8)

    # Set SSID
    packet[37] = len(ssid)
    packet.extend(ssid)

    # Set channel
    tail[12] = channel

    packet.extend(tail)
    return packet


def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)


def run(exit_check, channels=[1], ssids=RICK_SSIDS):
    if not len(channels) or not len(ssids):
        return

    disconnect()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ch_idx = 0
    idx = 0
    while True:
        is_exit = exit_check.check()
        if is_exit:
            break

        packet = make_packet(ssids[idx], channels[ch_idx])
        wlan.sendraw(packet)

        idx = (idx + 1) % len(ssids)
        ch_idx = (ch_idx + 1) % len(channels)

    disconnect()