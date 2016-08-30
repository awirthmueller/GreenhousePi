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

MODULE_NAME = 'Action_Trigger'
TABLE_NAME = 'action_triggers'
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

class Action_Trigger:
	ACTOR_TYPE = ''
	def __init__(self, actor_type,actor_id):
		self.initDB()
                self.ACTOR_TYPE = actor_type
		self.ACTOR_ID = actor_id		

	def initDB(self):
		conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
		logging.info(MODULE_NAME+": Successful DB connection")

		logging.info(MODULE_NAME+": Checking if db %s exists",DB_NAME)
		if DB_NAME not in list(r.db_list().run(conn)):
    			logging.info(MODULE_NAME+": db does not exist, creating...")
    			yield r.db_create(DB_NAME).run(conn)
		logging.info(MODULE_NAME+": db exists")

		logging.info(MODULE_NAME+": Checking to see if table %s exists",TABLE_NAME)
		if TABLE_NAME  not in list(r.table_list().run(conn)):
    			logging.info(MODULE_NAME+": table does not exist, creating...")
    			r.table_create(TABLE_NAME).run(conn)
		logging.info(MODULE_NAME+": table exists")
		conn.close()

	def writeAction(self,actiontype,actionvalue):
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
		d_trigger =    {'hostname':HOSTNAME,
				'actorid':self.ACTOR_ID,
                		'type':self.ACTOR_TYPE,
                		'actiontype':actiontype,
				'actionvalue':actionvalue,
                		'datetime':str(timestamp),
                                'action_state':'pending',
				'action_timestamp': None
				}
                r.table(TABLE_NAME).insert(d_trigger).run(conn, durability='soft')
                conn.close()
