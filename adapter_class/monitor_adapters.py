#!/usr/bin/python
# Copyright (c) 2016 Andreas Wirthmueller
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

import rethinkdb as r
import time
import datetime
import sys
from datetime import datetime

from config import HOSTNAME, DB_HOST, DB_PORT, DB_NAME
from BMP_adapter import BMP_Adapter
from DS18B20_adapter import DS18B20_Adapter
from Sunrise_Adapter import Sunrise_Adapter
from  TSL2591_adapter import  TSL2591_Adapter

MODULE_NAME = 'Readall_apaters'
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )
logging.info(MODULE_NAME+": ***************** Start ***************** ")

conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
logging.info(MODULE_NAME+": Successful DB connection")

logging.info(MODULE_NAME+": Checking if db %s exists",DB_NAME)
if DB_NAME not in list(r.db_list().run(conn)):
    logging.info(MODULE_NAME+"db does not exist, creating...")
    r.db_create(DB_NAME).run(conn)
logging.info(MODULE_NAME+": db exists")

logging.info(MODULE_NAME+": Checking to see if table %s exists",'observations')
if 'observations' not in list(r.table_list().run(conn)):
    logging.info(MODULE_NAME+": table does not exist, creating...")
    r.table_create("observations").run(conn)
logging.info(MODULE_NAME+": table exists")

timezone = time.strftime("%z")
reql_tz = r.make_timezone(timezone[:3] + ":" + timezone[3:])

# measure pressure
bmp = BMP_Adapter(350,'p_0001')

d_pressure = bmp.readJSON()

#print(d_pressure)

#measure temperature sensor 1
soil_temperature = DS18B20_Adapter('t_0001','28-04165b7853ff')
d_temp1 =  soil_temperature.readJSON()
#print(d_temp1)

#measure temperature sensor 2
outside_temperature = DS18B20_Adapter('t_0002','28-0316603aefff')
d_temp2 =  outside_temperature.readJSON()
#print(d_temp2)

plant_temperature = DS18B20_Adapter('t_0003','28-0316603ccdff')
d_temp3 =  plant_temperature.readJSON()
#print(d_temp3)

roof_temperature = DS18B20_Adapter('t_0004','28-04165b7988ff')
d_temp4 =  roof_temperature.readJSON()
#print(d_temp4)

lumen_sensor =  TSL2591_Adapter('lx_0001')
d_luminosity = lumen_sensor.readJSON()

#print(d_luminosity)

#get sunrise and sunset forcast
sunforcast = Sunrise_Adapter('s_0001','49.472816','11.399599')
d_sun = sunforcast.readJSON() 
#print(d_sun)

d_observation = {'pressure':[d_pressure],
		 'temperature':[d_temp1,d_temp2,d_temp3,d_temp4],
		 'luminosity':[d_luminosity],
		 'timestamp': str(datetime.now(reql_tz)),
		 'type':'sensors' 
                }

d_sunset = {'sunset':[d_sun],
            'timestamp': str(datetime.now(reql_tz)),
	    'type':'sunset'
	   }
logging.info(MODULE_NAME+": measurement %s",str(d_observation))

r.table("observations").insert(d_observation).run(conn, durability='soft') #Soft durability since losing one observation wouldn't be the end of the world.
#r.table("observations").insert(d_sunset).run(conn, durability='soft')
conn.close()
logging.info(MODULE_NAME+": measurements successfully written to db")
logging.info(MODULE_NAME+": ***************** End ***************** ")

