#!/usr/bin/env python

"""data_logger.py: docstring"""


__author__ = 'thomas'
__creation_date__ = '30.04.18'

import datetime

import python_general.library.configreader
import python_general.library.db.sqlite_db

COLUMNS = ['current_time', 'read_arg1', 'read_arg2', 'read_arg3', 'ret_arg1', 'ret_arg2', 'ret_arg3']


class DataLogger(python_general.library.configreader.ConfigReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Starting datalogger')
        self.config = self.config.get('co_detector').get(self.__class__.__name__.lower())
        self.db = python_general.library.db.sqlite_db.SQLite3Database(db_name=self.config.get('db_name'),
                                                                      db_path=self.config.get('db_path'))
        self.ensure_table()

    def ensure_table(self):
        if not self.db.check_table_exists(self.config.get('table_name')):
            self.log.warning('Table {} not existing, creating it with columns: {}'.format(self.config.get('table_name'),
                                                                                          COLUMNS))
            self.db.create_table(self.config.get('table_name'), COLUMNS,
                                 ['DATETIME', 'REAL', 'REAL', 'REAL', 'REAL', 'REAL', 'REAL'])

    def write_values(self, read_args, sensor_readings):
        values = [datetime.datetime.now(), *read_args, *sensor_readings]
        self.log.debug('Writing entry: {}'.format(values))
        self.db.insert_single_row(self.config.get('table_name'), values, COLUMNS)


if __name__ == '__main__':
    dl = DataLogger(config_file='../config.yml', loglevel='DEBUG')

