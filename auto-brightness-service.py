#!/usr/bin/env python

import dbus
import dbus.service
import sys
import signal

from PyQt4 import QtCore
from dbus.mainloop.qt import DBusQtMainLoop

from notifier import Notifier
from als import AmbientLightSensor
from brightnessctrl import BrightnessCtrl


class AutoBrightnessService(dbus.service.Object):
    def __init__(self):
        path = '/com/github/sheinz/autobrightness'
        bus_loop = DBusQtMainLoop(set_as_default=True)
        self._bus = dbus.SessionBus(mainloop=bus_loop)

        name = dbus.service.BusName('com.github.sheinz.autobrightness',
                                    bus=self._bus)

        dbus.service.Object.__init__(self, name, path)
        self.notifier = Notifier(self._bus)
        self._auto = False
        self._als = AmbientLightSensor()
        self._br_ctrl = BrightnessCtrl(self._bus)
        self._process_timer = QtCore.QTimer()
        self._process_timer.timeout.connect(self.process)

    @property
    def auto(self):
        return self._auto

    @auto.setter
    def auto(self, value):
        self._auto = value
        self.notifier.auto_brightness(self._auto)
        if self._auto:
            self._als.start()
            self._br_ctrl.start()
            self._process_timer.start(1000)
        else:
            self._als.stop()
            self._br_ctrl.stop()
            self._process_timer.stop()

    def process(self):
        value = self._als.get_value()
        print('Light sensor: %d' % value)
        if value == 0:
            value = 1
        self._br_ctrl.set_screen_brightness(value)
        if value < 5:
            self._br_ctrl.set_keyboard_light(True)
        else:
            self._br_ctrl.set_keyboard_light(False)

    def stop(self):
        self._process_timer.stop()
        self._als.stop()
        self._br_ctrl.stop()

    @dbus.service.method(dbus_interface='com.github.sheinz.autobrightness')
    def up(self):
        value = self._br_ctrl.screen_brightness_up()
        self.notifier.brightness(value)

    @dbus.service.method(dbus_interface='com.github.sheinz.autobrightness')
    def down(self):
        value = self._br_ctrl.screen_brightness_down()
        self.notifier.brightness(value)

    @dbus.service.method(dbus_interface='com.github.sheinz.autobrightness')
    def auto_toggle(self):
        self.auto = not self.auto

    @dbus.service.method(dbus_interface='com.github.sheinz.autobrightness')
    def exit(self):
        sys.exit()


class Application(QtCore.QCoreApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self._auto_br = AutoBrightnessService()

    def event(self, e):
        return super(Application, self).event(e)

    def quit(self):
        self._auto_br.stop()
        super(Application, self).quit()


def main():
    app = Application(sys.argv)
    app.startTimer(1000)
    signal.signal(signal.SIGINT, lambda *args: app.quit())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
