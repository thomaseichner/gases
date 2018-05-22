#!/usr/bin/env python

"""thdetector.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '14.05.18'


import time

import python_general.tools.detectorskeleton

import sensor_reader
import tools.data_logger


class THDetector(python_general.tools.detectorskeleton.DetectorSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def startup(self, *args, **kwargs):
        self.log.info('Starting detector')
        self.sr = sensor_reader.SensorReader(*args, **kwargs)
        self.dl = tools.data_logger.DataLogger(*args, **kwargs)


if __name__ == '__main__':
    cod = THDetector(config_file='/home/thomas/blog/gases/gases/config.yml', loglevel='DEBUG',
                     config_toplevel='th_detector')
    cod.run_cycles(100)
