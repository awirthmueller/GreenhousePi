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
import Adafruit_BMP.BMP085 as BMP085


MODULE_NAME = 'BMP_Adapter'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

class BMP_Adapter:
        SENSOR_TYPE = "pressure"
        MEASURE_T="Celsius"
        MEASURE_P="hPa"
        MEASURE_H="m"

        #contains altitude above sealevel in meters of the sensors location
        altitude = 0
        sensor_id = ''

        def __init__(self, altitude,sensor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                self.altitude = altitude
                #intialize the sensor in read mode standard
                self.sensor = BMP085.BMP085()

                # You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
                # BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
                # datasheet for more details on the meanings of each mode (accuracy and power
                # consumption are primarily the differences).  The default mode is STANDARD.
                sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

                self.sensor_id = sensor_id
                logging.info(MODULE_NAME +": constructor exit")
        def read(self):
                temp = self.sensor.read_temperature()
                pressure = self.sensor.read_pressure()
                psea = self.sensor.read_sealevel_pressure(self.altitude)
                return temp,pressure/100,psea/100,self.altitude
        def readJSON(self):
	        temp,pressure,psea,altitude = self.read()	
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_pressure = 	{'hostname':HOSTNAME,
             			'type':self.SENSOR_TYPE,
             			'sensorid':self.sensor_id,
             			'temp':temp,
             			'pressure_sea':psea,
             			'measure_pressure':self.MEASURE_P,
             			'altitude':self.altitude,
             			'measure_temp':self.MEASURE_T,
             			'measure_altitude':self.MEASURE_H,
             			'datetime':str(timestamp)}
		return d_pressure
	
