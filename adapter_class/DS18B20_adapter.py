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

import time
import datetime
from datetime import datetime
from config import HOSTNAME

import logging

MODULE_NAME = 'DS18B20'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/sensors/log/adapter_log.log'
    )

class DS18B20_Adapter:
        SENSOR_TYPE = "temperature"
        MEASURE_T="Celsius"

        def __init__(self, sensor_id,slave_id):
                logging.info(MODULE_NAME+ ": constructor start")

                self.sensor_id = sensor_id
		self.slave_id = slave_id
                logging.info(MODULE_NAME +": constructor exit")


	def read(self):
    		# 1-wire Slave Datei lesen
    		filename = '/sys/bus/w1/devices/' + self.slave_id + '/w1_slave'
    		file = open(filename)
    		filecontent = file.read()
    		file.close()

    		# Temperaturwerte auslesen und konvertieren
    		stringvalue = filecontent.split("\n")[1].split(" ")[9]
    		temperature = float(stringvalue[2:]) / 1000

    		# Temperatur ausgeben
    		rueckgabewert = '%6.2f' % temperature
    		return(rueckgabewert)
        def readJSON(self):
                temp = self.read()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_temp = 	{'hostname':HOSTNAME,
             			'type':self.SENSOR_TYPE,
             			'sensorid':self.sensor_id,
             			'temp':temp,
             			'datetime':str(timestamp)}
		return d_temp

