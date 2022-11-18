RickRoll Wristband
==================

[![](https://img.youtube.com/vi/4qXFLblkhrk/0.jpg)](https://youtu.be/4qXFLblkhrk)

## What is it?

This is a project of a wearable watch with a secret
[rickroll spam](https://github.com/spacehuhn/esp8266_beaconSpam) Wi-Fi function based on a 
[LilyGo T-Wristband](https://www.lilygo.cc/products/t-wristband) device.
The watch uses deepsleep mode to reduce power consuption and also has
debug mode, that loads webrepl via Wi-Fi (station or access point mode).

This repository contains:
- Custom MicroPython-1.19.1 [firmware](https://github.com/zmactep/rickroll-wristband/tree/master/firmware) for ESP32
- Instruction how to build your own for a different version
- A [code](https://github.com/zmactep/rickroll-wristband/tree/master/src) of watch app with rickroll function

## Special thanks

- MicroPython ([micropython/micropython](https://github.com/micropython/micropython))
- ST7789_mpy ([russhughes/st7789_mpy](https://github.com/russhughes/st7789_mpy))

## How to build

### Step 1

Download last MicroPython stable version (e.g. 1.9.1), st7789_mpy driver and esp-idf tool:
```bash
git clone -b v1.9.1 https://github.com/micropython/micropython.git
git clone https://github.com/russhughes/st7789_mpy.git
git clone -b v4.4.3 --recursive https://github.com/espressif/esp-idf.git
```

### Step 2

Install `esp-idf` and activate it. **Make sure that you use non-virtualenv python.**
```bash
cd esp-idf
./install.sh
. ./export.sh
cd ..
```

### Step 3

Build `mpy-cross` tool:
```bash
cd micropython/mpy-cross
make
cd ../..
```

### Step 4

Insert two additional functions into ESP32 `network.WLAN`: `esp_wifi_set_channel` and `esp_wifi_80211_tx`. The first one is used
to select specific channel and the second we can use to transfer some raw data package.
You can find a place to put them at `micropython/ports/esp32/network_wlan.c`.
If you use `1.19.1` version of MicroPython you can simple apply the [patch](https://github.com/zmactep/rickroll-wristband/blob/master/network_wlan.c.patch) in this repo. Otherwise you have to add two includes:
```c
#include "py/objarray.h"
#include "py/binary.h"
```

And two functions:
```c
STATIC mp_obj_t network_wlan_channel(mp_obj_t self_in, mp_obj_t channel) {
    wifi_mode_t mode;
    esp_exceptions(esp_wifi_get_mode(&mode));
    if ((mode & WIFI_MODE_STA) == 0) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("STA must be active"));
    }

    mp_int_t wifi_channel = 0;
    if (mp_obj_get_int_maybe(channel, &wifi_channel)) {
        esp_exceptions(esp_wifi_set_channel(wifi_channel, WIFI_SECOND_CHAN_NONE));
    } else {
        mp_raise_msg(&mp_type_TypeError, MP_ERROR_TEXT("Channel must be integer value"));
    }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(network_wlan_channel_obj, network_wlan_channel);
```

```c
STATIC mp_obj_t network_wlan_sendraw(size_t n_args, const mp_obj_t *args) {
    wifi_mode_t mode;
    esp_exceptions(esp_wifi_get_mode(&mode));

    bool en_sys_seq = 0;
    if (n_args == 3) {
        en_sys_seq = mp_obj_is_true(args[2]);
    }

    mp_obj_array_t* a_ptr = MP_OBJ_TO_PTR(args[1]);
    if (a_ptr->typecode != BYTEARRAY_TYPECODE) {
        mp_raise_msg(&mp_type_TypeError, MP_ERROR_TEXT("Package must be a bytestring"));
    }

    byte* packet = (byte*)a_ptr->items;
    size_t packet_len = a_ptr->len;

    int result = esp_wifi_80211_tx(mode & WIFI_MODE_STA ? ESP_IF_WIFI_STA : ESP_IF_WIFI_AP, packet, packet_len, en_sys_seq);

    return mp_obj_new_int(result);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(network_wlan_sendraw_obj, 2, 3, network_wlan_sendraw);
```

You also have to add function objects into methods table:
```c
STATIC const mp_rom_map_elem_t wlan_if_locals_dict_table[] = {
    ...
     { MP_ROM_QSTR(MP_QSTR_channel), MP_ROM_PTR(&network_wlan_channel_obj) },
     { MP_ROM_QSTR(MP_QSTR_sendraw), MP_ROM_PTR(&network_wlan_sendraw_obj) },
};
```

### Step 5

Copy some fonts from [st7789 c-module](https://github.com/russhughes/st7789_mpy):
```bash
cp st7789_mpy/fonts/bitmap/vga2_*.py micropython/ports/esp32/modules/
```

And build the firmware:
```bash
make USER_C_MODULES=../../../../st7789_mpy/st7789/micropython.cmake FROZEN_MANIFEST="" FROZEN_MPY_DIR=./modules
```