#!/usr/bin/env python

"""data_logger.py: docstring"""


__author__ = 'thomas'
__creation_date__ = '30.04.18'


import python_general.tools.data_logger
import python_general.library.db.sqlite_db


class DataLogger(python_general.tools.data_logger.DataLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Starting datalogger for {}'.format(kwargs.get('config_toplevel')))
        self.config = self.config.get(kwargs.get('config_toplevel')).get(self.__class__.__name__.lower())
        self.log.info('Opening DB: {}: {}'.format(self.config.get('db_path'), self.config.get('db_name')))
        self.db = python_general.library.db.sqlite_db.SQLite3Database(db_name=self.config.get('db_name'),
                                                                      db_path=self.config.get('db_path'))

        self.ensure_table()


if __name__ == '__main__':
    dl = DataLogger(config_file='../config.yml', loglevel='DEBUG', config_toplevel='co_detector')

