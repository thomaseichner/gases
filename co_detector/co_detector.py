#!/usr/bin/env python

"""co_detector.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '26.04.18'


import time

import python_general.tools.singleton

import sensor_reader
import data_logger


class CODetector(python_general.tools.singleton.Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Starting controlflow')
        self.config = self.config.get('co_detector').get(self.__class__.__name__.lower())
        self.start_control(*args, **kwargs)

    def startup(self, *args, **kwargs):
            self.log.info('Starting detector')
            self.sr = sensor_reader.SensorReader(*args, **kwargs)
            self.dl = data_logger.DataLogger(*args, **kwargs)


    @property
    def read_arguments(self):
        return self.config.get('read_arguments')

    def run_once(self):
        self.log.debug('Starting single cycle')
        values = self.sr.read_value(self.read_arguments)
        self.dl.write_values(self.read_arguments, values)
        return values

    def run_cycles(self, max_cycles=float('inf')):
        current_cycle = 0
        try:
            while current_cycle < max_cycles:
                self.log.info('Starting cycle {} of {}'.format(current_cycle, max_cycles))
                self.update_status_file()
                ret = self.run_once()
                self.log.info('Asked: {}, Sensor return: {}'.format(self.read_arguments, ret))
                current_cycle += 1
                time.sleep(self.config.get('readout_interval'))
        finally:
            self.delete_status_file()

if __name__ == '__main__':
    cod = CODetector(config_file='/home/thomas/blog/gases/gases/config.yml', loglevel='DEBUG')
    cod.run_cycles(100)
