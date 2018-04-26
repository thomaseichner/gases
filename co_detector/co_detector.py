#!/usr/bin/env python

"""co_detector.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '26.04.18'


import time

import python_general.library.configreader

import sensor_reader


class CODetector(python_general.library.configreader.ConfigReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Starting detector')
        self.config = self.config.get('co_detector').get(self.__class__.__name__.lower())
        self.sr = sensor_reader.SensorReader(*args, **kwargs)

    @property
    def read_arguments(self):
        return self.config.get('read_arguments')

    def run_once(self):
        self.log.debug('Starting single cycle')
        return self.sr.read_value(self.read_arguments)

    def run_cycles(self, max_cycles=float('inf')):
        current_cycle = 0
        while current_cycle < max_cycles:
            self.log.info('Starting cycle {} of {}'.format(current_cycle, max_cycles))
            ret = self.run_once()
            self.log.info('Asked: {}, Sensor return: {}'.format(self.read_arguments, ret))
            current_cycle += 1
            time.sleep(self.config.get('readout_interval'))


if __name__ == '__main__':
    cod = CODetector(config_file='../config.yml', loglevel='DEBUG')
    cod.run_cycles(10)
