#!/usr/bin/python
# Copyright (c) 2016 
# Author: Andreas Wirthmueller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import logging
import time
import datetime
from datetime import datetime
from config import HOSTNAME
import tsl2591


MODULE_NAME = 'TSL2591_Adapter'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

class TSL2591_Adapter:
        SENSOR_TYPE = "light"
        MEASURE_L="lux"

     
        def __init__(self, sensor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                #intialize the sensor
                self.sensor = tsl2591.Tsl2591()  # initialize

                self.sensor_id = sensor_id
                logging.info(MODULE_NAME +": constructor exit")
        def read(self):
                full,ir = self.sensor.get_full_luminosity()
                lux = self.sensor.calculate_lux(full, ir)
                return full,ir,lux
        def readJSON(self):
	        full,ir,lux = self.read()	
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_pressure = 	{'hostname':HOSTNAME,
             			'type':self.SENSOR_TYPE,
             			'sensorid':self.sensor_id,
             			'luminosity':lux,
				'full_spectrum (raw)':full,
				'ir_spectrum (raw)':ir,
             			'measure_light':self.MEASURE_L,
             			'datetime':str(timestamp)}
		return d_pressure
	
