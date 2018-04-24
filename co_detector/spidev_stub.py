#!/usr/bin/env python

"""spidev_stub.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '24.04.18'


class SpiDev():
    def __init__(self):
        pass

    def open(self, channel, bus):
        pass

    def xfer2(self, input_list):
        assert len(input_list) == 3
        return list(reversed(input_list))