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
from dateutil import tz
from dateutil import parser
import urllib2
import json
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal

from config import HOSTNAME


MODULE_NAME = 'SUNRISE_Adapter'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/sensors/log/adapter_log.log'
    )

class Sunrise_Adapter:
	SENSOR_TYPE = "sunposition"
	MEASURE_T="time"
        LAT = '49.472816'
	LONG = '11.399599' 

	#contains altitude above sealevel in meters of the sensors location
        altitude = 0
        sensor_id = ''

        def __init__(self, sensor_id, lat, long):
                logging.info(MODULE_NAME+ ": constructor start")
                self.LAT = lat
                self.LONG = long 
                self.sensor_id = sensor_id
                logging.info(MODULE_NAME +": constructor exit")

        def read(self):
	        request_string = 'http://api.sunrise-sunset.org/json?lat='+self.LAT+'&lng='+self.LONG+'&date=today&formatted=0'
        	# put request out
        	response = urllib2.urlopen(request_string)
        	# read json reponse
        	data = json.load(response)
        	# get local timezone
        	local_timezone = tzlocal.get_localzone() # get pytz tzinfo

        	#read sunset and sunrise times from response (in UTC)
        	sunrise = parser.parse(data['results']['sunrise'])
        	sunset = parser.parse(data['results']['sunset'])

        	#change times from UTC to local time
        	sunrise.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        	sunset.replace(tzinfo=pytz.utc).astimezone(local_timezone)

        	return(sunrise,sunset)

        def readJSON(self):
	        sunrise,sunset = self.read()	
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_sunset = 	{'hostname':HOSTNAME,
             			'type':self.SENSOR_TYPE,
             			'sensorid':self.sensor_id,
             		        'latitude':self.LAT,
				'longtitude':self.LONG, 
				'sunset':sunset,
				'sunrise':sunrise,	
             			'datetime':str(timestamp)}
		return d_sunset
	
