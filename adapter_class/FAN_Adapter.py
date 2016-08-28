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
from config import HOSTNAME
import RPi.GPIO as GPIO

MODULE_NAME = 'FAN_Adapter'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/sensors/log/adapter_log.log'
    )

class FAN_Adapter:

	def __init__(self, gpio, actor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                self.actor_id = actor_id
                self.gpio = gpio
		GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(gpio, GPIO.OUT)
		logging.info(MODULE_NAME +": constructor exit")

        def set_on(self):
		GPIO.output(self.gpio, GPIO.HIGH)
		logging.info(MODULE_NAME+ ": fan on")

	def set_off(self):
		GPIO.output(self.gpio, GPIO.LOW)
		logging.info(MODULE_NAME+ ": fan off")

