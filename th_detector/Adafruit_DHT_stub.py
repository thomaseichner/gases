#!/usr/bin/env python

"""Adafruit_DHT_stub.py: docstring"""

__author__ = 'thomas'
__creation_date__ = '14.05.18'

import random

def read_retry(model, pin):
    humidity = random.gauss(model, 2)
    temp = random.gauss(pin, 2)
    return humidity, temp