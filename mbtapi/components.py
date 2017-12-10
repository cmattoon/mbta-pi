# -*- coding: utf-8 -*-

import gc
import pyb


class WS2812B(object):
    """
    WS2812B Driver
    """

    buf_bytes = (0x11, 0x13, 0x31, 0x33)

    def __init__(self, spi_bus=1, nLEDs=1, intensity=1):
        self.intensity = min(1, max(0, float(intensity)))
        self.nLEDs = max(0, int(nLEDs))
        
        # Buffer Length: 3 bytes for each color
        self.bufLen = self.nLEDs * 3

        self.buf = bytearray(self.bufLen)

        self.spi = pyb.SPI(spi_bus,
                           pyb.SPI.MASTER,
                           baudrate=kwargs.pop(
        
    
    
