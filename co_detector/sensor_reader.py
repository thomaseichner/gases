#!/usr/bin/env python

"""sensor_reader.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '24.04.18'

try:
    import spidev
except:
    import spidev_stub as spidev

import python_general.library.configreader

class SensorReader(python_general.library.configreader.ConfigReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self.config.get('co_detector').get(self.__class__.__name__.lower())
        self.sd = spidev.SpiDev()
        self.log.info("Opening to: {}, {}".format(self.config.get('channel'), self.config.get('bus')))
        self.sd.open(self.config.get('channel'), self.config.get('bus'))

    def read_value(self):
        self.log.debug("Reading values with config: {}".format(self.config.get('read_arguments')))
        ret = self.sd.xfer2(self.config.get('read_arguments'))
        self.log.debug("Got answer: {}".format(ret))
        return ret

if __name__ == '__main__':
    sr = SensorReader(config_file="../config.yml", loglevel='DEBUG')
    print(sr.read_value())
