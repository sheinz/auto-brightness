#!/usr/bin/env python

import dbus


class BrightnessCtrl(object):
    def __init__(self, bus):
        self._bus = bus
        self._proxy = self._bus.get_object('org.gnome.SettingsDaemon',
                                           '/org/gnome/SettingsDaemon/Power')

        self._screen_if = dbus.Interface(self._proxy,
                                         'org.gnome.SettingsDaemon.Power.Screen')

        self._kb_if = dbus.Interface(self._proxy,
                                     'org.gnome.SettingsDaemon.Power.Keyboard')

        self._kb_light_on = False

    def set_screen_brightness(self, value):
        self._screen_if.SetPercentage(value)

    def screen_brightness_up(self):
        r = self._screen_if.StepUp()
        return int(r)

    def screen_brightness_down(self):
        r = self._screen_if.StepDown()
        return int(r)

    def set_keyboard_light(self, on):
        if on != self._kb_light_on:
            self._kb_light_on = on
            if self._kb_light_on:
                self._kb_if.StepUp()
            else:
                while int(self._kb_if.StepDown()) != 0:
                    pass
