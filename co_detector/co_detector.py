#!/usr/bin/env python

"""co_detector.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '26.04.18'


import time
import os
import datetime
import sys

import python_general.library.configreader

import sensor_reader
import data_logger


class CODetector(python_general.library.configreader.ConfigReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Starting controlflow')
        self.config = self.config.get('co_detector').get(self.__class__.__name__.lower())
        self.startup(*args, **kwargs)

    def startup(self, *args, **kwargs):
        if self.check_for_running():
            self.log.info('Program is already running, exiting attempt')
            sys.exit()
        else:
            self.log.info('Starting detector')
            self.sr = sensor_reader.SensorReader(*args, **kwargs)
            self.dl = data_logger.DataLogger(*args, **kwargs)

    def check_for_running(self):
        files = self.get_status_files()
        filedates = [i.split('_')[1] for i in files]
        filedates = [datetime.datetime.strptime(i, self.config.get('time_format')) for i in filedates]
        file_found = False
        for filedate in filedates:
            if (datetime.datetime.now() - filedate) <= datetime.timedelta(minutes=5):
                file_found = True
        return file_found

    def get_status_files(self):
        files = [i for i in os.listdir(self.tmp_path) if i.startswith(self.config.get('running_identifier'))]
        return files

    @property
    def read_arguments(self):
        return self.config.get('read_arguments')

    @property
    def tmp_path(self):
        return self.config.get('tmpfolder', '.')

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

    def update_status_file(self):
        self.delete_status_file()
        open(os.path.join(self.tmp_path, '{}_{}'.format(self.config.get('running_identifier'),
                                                    datetime.datetime.now().strftime(self.config.get('time_format')))), 'w').close()

    def delete_status_file(self):
        existing_files = self.get_status_files()
        self.log.debug('Found existing files: {}'.format(existing_files))
        for file in existing_files:
            os.remove(os.path.join(self.tmp_path, file))


if __name__ == '__main__':
    cod = CODetector(config_file='/home/thomas/blog/gases/gases/config.yml', loglevel='DEBUG')
    cod.run_cycles(100)
