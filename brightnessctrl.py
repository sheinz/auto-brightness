#!/usr/bin/env python

import dbus
from time import sleep
from stoppable_thread import StoppableThread


class BrightnessCtrl(StoppableThread):
    def __init__(self, bus):
        super(BrightnessCtrl, self).__init__()
        self._bus = bus
        self._proxy = self._bus.get_object('org.gnome.SettingsDaemon',
                                           '/org/gnome/SettingsDaemon/Power')

        self._screen_if = dbus.Interface(self._proxy,
                                         'org.gnome.SettingsDaemon.Power.Screen')

        self._kb_if = dbus.Interface(self._proxy,
                                     'org.gnome.SettingsDaemon.Power.Keyboard')
        self._kb_light_on = False
        self._screen_brightness = None
        self._screen_desired_brightness = None

    def run(self):
        if self._screen_brightness != self._screen_desired_brightness:
            if self._screen_desired_brightness > self._screen_brightness:
                self._screen_brightness += 1
            else:
                self._screen_brightness -= 1
            print('Setting brightness: %d' % self._screen_brightness)
            self._screen_if.SetPercentage(self._screen_brightness)
        sleep(0.4)

    def set_screen_brightness(self, value):
        if self._screen_brightness is None:
            self._screen_brightness = value
            self._screen_desired_brightness = value
            self._screen_if.SetPercentage(value)
        else:
            self._screen_desired_brightness = value

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
