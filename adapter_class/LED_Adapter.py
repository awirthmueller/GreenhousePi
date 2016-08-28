import time
import threading
import RPi.GPIO as GPIO
from datetime import datetime
from config import HOSTNAME

from threading import Thread


class LED_Adapter:
	ACTOR_TYPE = 'LED'
        def __init__(self, gpio, actor_id):
		self.gpio = gpio
		self.actor_id = actor_id
		self.t_bstop = threading.Event()
		self.t_wstop2 = threading.Event()
		self.t_wstop = threading.Event()
	        GPIO.setwarnings(False) 
		GPIO.setmode(GPIO.BOARD)	
		GPIO.setup(gpio, GPIO.OUT)
		GPIO.output(self.gpio, GPIO.LOW)
		self.status = 'Off'
		
		
	def set_on(self):
		self.t_bstop.set()
                self.t_wstop.set()
		GPIO.output(self.gpio, GPIO.HIGH)
		self.status = 'On'

	def set_off(self):
		self.t_bstop.set()
		self.t_wstop.set()
		GPIO.output(self.gpio, GPIO.LOW)
		self.status = 'Off'

	def blinker(self,t,duty_cycle):
	 try:
    	        while(not self.t_bstop.is_set()):
	                GPIO.output(self.gpio, GPIO.HIGH)
    		        event_is_set = self.t_bstop.wait(t*duty_cycle)
			if (event_is_set):
				break
		        GPIO.output(self.gpio, GPIO.LOW)
                        if (event_is_set):
                                break
                        event_is_set = self.t_bstop.wait(t*(1-duty_cycle))
		self.bstopped = True
	 except:
	        pass 

        def wait_blinker(self,wait_time,interval_time,duty_cycle):
	 try:
                actual_wait = wait_time / 2.0
                actual_interval = interval_time / 2.0
		while(not self.t_wstop.is_set() and actual_interval >  0.0625):
		        print('Actual Wait:' + str(actual_wait))
			print('Actual Blink:' + str(actual_interval)) 
			self.t_bstop.set()
			self.t_wstop.wait(.1)	
			self.blink(actual_interval,duty_cycle)
			self.t_wstop.wait(actual_wait)
			actual_wait = actual_wait / 2.0
			actual_interval = actual_interval / 2.0
		self.t_bstop.set()
		self.t_wstop.set()

		while (not self.bstopped):
                	self.t_wstop.wait(.1)
		GPIO.output(self.gpio, GPIO.HIGH)
		self.wstopped = True 
         except:
		pass

        def wait_blinker2(self,wait_time,interval_time):
	  try:
                actual_wait = wait_time / 4.0
                actual_duty = 0.1
                while(not self.t_wstop2.is_set() and actual_wait >  0.95):
                        print('Actual Blink:' + str(actual_wait))
                        self.t_bstop.set()
                        self.t_wstop2.wait(.1)
                        self.blink(interval_time,actual_duty)
                        self.t_wstop2.wait(actual_wait)
                        actual_wait = actual_wait / 4.0
                        actual_duty = actual_duty + ((1 - actual_duty) * 0.25)
                self.t_bstop.set()
                self.t_wstop.set()
		self.t_wstop2.set()
                while (not self.bstopped):
                        self.t_wstop.wait(.1)
                GPIO.output(self.gpio, GPIO.HIGH)
                self.wstopped = True
	  except:
		pass

	def blink(self,time,duty_cycle):
		self.t_bstop.clear()
		self.bstopped = False	
	    	t = Thread(target=self.blinker, args=(time,duty_cycle,))
		t.setDaemon(True)
    		t.start()
		self.status = 'Blink'

	def blink_wait(self,wait_time,interval_time,duty_cycle):
		self.t_wstop.clear()
		self.wstopped = False
		w = Thread(target=self.wait_blinker, args=(wait_time,interval_time,duty_cycle))
		w.setDaemon(True)
                w.start()
		self.status = 'Blink'

        def blink_wait2(self,wait_time,interval_time):
                self.t_wstop2.clear()
                self.wstopped2 = False
                w = Thread(target=self.wait_blinker2, args=(wait_time,interval_time))
                w.setDaemon(True)
                w.start()
		self.status = 'Blink'

        def blink_stop(self):
	 	self.t_bstop.set()
		self.t_wstop.set()
	        GPIO.output(self.gpio, GPIO.LOW)	
		self.status = 'Off'

        def readJSON(self):
                self.status = GPIO.input(self.gpio)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_led     =    {'hostname':HOSTNAME,
                                'type':self.ACTOR_TYPE,
                                'actorid':self.actor_id,
                                'state':self.status,
                                'datetime':str(timestamp)}
                return d_led
			
