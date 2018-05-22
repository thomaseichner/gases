#!/usr/bin/env python

"""co_detector.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '26.04.18'


import time

import python_general.tools.detectorskeleton

import sensor_reader
import tools.data_logger


class CODetector(python_general.tools.detectorskeleton.DetectorSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def startup(self, *args, **kwargs):
            self.log.info('Starting detector')
            self.sr = sensor_reader.SensorReader(*args, **kwargs)
            self.dl = tools.data_logger.DataLogger(*args, **kwargs)


if __name__ == '__main__':
    cod = CODetector(config_file='/home/thomas/blog/gases/gases/config.yml', loglevel='DEBUG',
                     config_toplevel='co_detector')
    cod.run_cycles(100)
