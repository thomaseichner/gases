#!/usr/bin/env python

"""sensor_reader.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '14.05.18'


try:
    import Adafruit_DHT
except:
    import Adafruit_DHT_stub as Adafruit_DHT

import python_general.library.configreader


class SensorReader(python_general.library.configreader.ConfigReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self.config.get('th_detector').get(self.__class__.__name__.lower())

    def read_value(self):
        self.log.debug("Reading values with config: ({}, {})".format(self.config.get('model'), self.config.get('pin')))
        ret = Adafruit_DHT.read_retry(self.config.get('model'), self.config.get('pin'))
        self.log.debug("Got answer: {}".format(ret))
        return ret


if __name__ == '__main__':
    sr = SensorReader(config_file="../config.yml", loglevel='DEBUG')
    print(sr.read_value())
