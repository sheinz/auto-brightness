#!/usr/bin/env python

import dbus


class Notifier(object):
    def __init__(self, bus):
        self._app_name = 'auto_brightness_service'
        self._bus = bus
        self._proxy = self._bus.get_object('org.freedesktop.Notifications',
                                           '/org/freedesktop/Notifications')

        self._interface = dbus.Interface(self._proxy,
                                         'org.freedesktop.Notifications')

    def _get_brightness_icon(self, value):
        icons = ('notification-display-brightness-off',
                 'notification-display-brightness-low',
                 'notification-display-brightness-medium',
                 'notification-display-brightness-high',
                 'notification-display-brightness-full')
        if value < 10:
            return icons[0]
        elif value < 30:
            return icons[1]
        elif value < 70:
            return icons[2]
        elif value < 90:
            return icons[3]
        else:
            return icons[4]

    def notify(self, title, text, icon):
        self._interface.Notify(self._app_name, 0, icon,
                               title, text, [], {}, -1)

    def brightness(self, level):
        icon = self._get_brightness_icon(level)
        data = {'x-canonical-private-synchronous': 'brightness', 'value': level}
        self._interface.Notify(self._app_name, 0, icon, ' ', '', [], data, -1)

    def auto_brightness(self, on):
        if on:
            icon = self._get_brightness_icon(50)
            text = 'Auto brightness ON'
        else:
            icon = self._get_brightness_icon(0)
            text = 'Auto brightness OFF'
        data = {'x-canonical-private-synchronous': ''}
        self._interface.Notify(self._app_name, 0, icon, text, '', [], data, -1)
