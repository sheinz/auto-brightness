#!/usr/bin/env python

from time import sleep
from collections import deque
from stoppable_thread import StoppableThread


class AmbientLightSensor(StoppableThread):
    def __init__(self):
        super(AmbientLightSensor, self).__init__()
        self._max_value = 7880
        self._filter_depth = 10
        self._filter = deque(self._filter_depth * [50.0], self._filter_depth)
        self._value = None
        self._sensor_data_file = '/sys/bus/acpi/devices/ACPI0008:00/ali'

    def run(self):
        with open(self._sensor_data_file) as f:
            raw = f.read()
            value = 100.0 - 1000.0 / (float(raw)/3 + 10.0)
            self._filter.append(value)
            self._filter.popleft()
            self._value = int(round(sum(self._filter) / len(self._filter)))
        sleep(2)

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
