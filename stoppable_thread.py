#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread, Event


class StoppableThread(object):
    def __init__(self):
        self._stop = Event()
        self._stop.set()

    def _run(self):
        while not self._stop.isSet():
            self.run()

    def run(self):
        pass

    def stop(self):
        self._stop.set()

    def start(self):
        if self._stop.isSet():
            self._stop.clear()
            self._thread = Thread(target=self._run)
            self._thread.start()
