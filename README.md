# Automatic brightness

Automatic display brightness controller for ASUS Zenbook UX303
The service runs in background and adjusts screen brightness and 
keyboard backlight depending on ambient light sensor data.

It requires ALS [ALS](https://github.com/danieleds/als) driver.

If driver works correctly the file `/sys/bus/acpi/devices/ACPI0008:00/ali`
should be present and contain Ambient Light Sensor value.

Automatic brightness adjustment consists of two parts:
  * **auto-brightness-service.py** - Service that must be run in background.
  * **auto-brightness-ctrl.py** - Control utility. Used to tunr on/off 
    automatic brightness adjustment. Also used to manually adjust screen
    brightness if auto mode is off.

Tested with:
---
  * Asus Zenbook UX303UA
  * Ubuntu 15.10 x64
