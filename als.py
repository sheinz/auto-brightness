#!/usr/bin/env python

import threading
from time import sleep
from collections import deque


class AmbientLightSensor(object):
    def __init__(self):
        self._max_value = 7880
        self._filter_depth = 20
        self._filter = deque(self._filter_depth * [50], self._filter_depth)
        self._value = None
        self._sensor_data_file = '/sys/bus/acpi/devices/ACPI0008:00/ali'
        self._stop = threading.Event()
        self._thread = None

    def stop(self):
        self._stop.set()

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def run(self):
        while not self._stop.isSet():
            with open(self._sensor_data_file) as f:
                raw = f.read()
                value = 100.0 - 1000.0 / (float(raw)/3 + 10.0)
                self._filter.append(int(value))
                self._filter.popleft()
                self._value = int(sum(self._filter) / len(self._filter))
            sleep(1)

    def get_raw(self):
        with open(self._sensor_data_file) as f:
            value = f.read()
            return int(value)

    def get_value(self):
        return self._value

if __name__ == "__main__":
    als = AmbientLightSensor()
    try:
        als.start()
        while True:
            value = als.get_value()
            if value is not None:
                print("%d : %d" % (als.get_raw(), als.get_value()))
            else:
                print('waiting...')
            sleep(0.5)
    except KeyboardInterrupt:
        als.stop()
