
#General stuff
import datetime
import logging
import sys

#For tornado server 

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.websocket
import tornado.httpserver
from tornado.options import define, options, parse_command_line

#For rethink stuff
import rethinkdb as r #For db stuff
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

#For project configuration 
from config import * 

from Action_Trigger import Action_Trigger


define("port", default=8888, help="run on the given port", type=int)

# setup logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
datefmt='%m-%d %H:%M',
filename='/home/pi/GreenMon/log/tornado_log.log'
)

#create db connection
conn = r.connect(DB_HOST,DB_PORT,DB_NAME) 

#clients connecting to the server
clients = set()

def dbSetup():
	logging.info("Attempting db connection to %s:%s:%s...",DB_HOST,DB_PORT,DB_NAME)

	logging.info("Checking if db %s exists",DB_NAME)
	if DB_NAME not in list(r.db_list().run(conn)):
    		logging.info("db does not exist, creating...")
    		r.db_create(DB_NAME).run(conn)
	logging.info("db exists")
	logging.info("Checking to see if table %s exists",'observations')
	if 'observations' not in list(r.table_list().run(conn)):
    		logging.info("table does not exist, creating...")
    		r.table_create("observations").run(conn)
        conn.close()
	logging.info("table exists")

#There is a loop type in python rethinkDB client.set it to tornado
r.set_loop_type("tornado")


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("This is your response")
        self.finish()

class WSocketHandler(tornado.websocket.WebSocketHandler): #Tornado Websocket Handler
    def check_origin(self, origin):
        return True

    @tornado.gen.coroutine
    def on_message(self,message):
	try:
		logging.info("on_message::entering")
		if (message == "f_0001 ON"):
			 logging.info("on_message::FAN f_0001 ON received")
			 trigger_action('Fan','f_0001','Switch','On')
                if (message == "f_0001 OFF"):
                         logging.info("on_message::FAN f_0001 OFF received")
                         trigger_action('Fan','f_0001','Switch','Off')
                if (message == "a_0001 ON"):
                         logging.info("on_message::Automation switch a_0001 ON received")
                if (message == "a_0001 OFF"):
                         logging.info("on_message::Automation switch a_0001 OFF received")
	except:
            	exc_type, exc_value, exc_traceback = sys.exc_info()
            	logging.info("on_message::exception %s %s %s",exc_type, exc_value, exc_traceback)
       		pass

    def open(self):
        self.stream.set_nodelay(True)
        logging.info("WScoketHandler::calling send_initial_data")
	send_initial_data(self)
	clients.add(self) 
        logging.info("WScoketHandler::client joined")

    def on_close(self):
        if self in clients:
        	clients.remove(self) #Remove client


@tornado.gen.coroutine
def trigger_action(actor_type,actor_id,action_type,parameter):
	try:
            logging.info("trigger_action::"+str(actor_type)+' '+str(actor_id) + ' '  + str(action_type) + ' ' + str(parameter))
	    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = yield r.connect(DB_HOST, DB_PORT, DB_NAME)
            d_trigger =    {'hostname':HOSTNAME,
                            'actorid':actor_id,
                            'type':actor_type,
                            'actiontype':action_type,
                            'actionvalue':parameter,
                            'datetime':str(timestamp),
                            'action_state':'pending',
                            'action_timestamp': None
                            }
            yield r.table('action_triggers').insert(d_trigger).run(conn, durability='soft')
            conn.close()
	    logging.info("trigger_action written::"+str(actor_type)+' '+str(actor_id) + ' '  + str(action_type) + ' ' + str(parameter))
	except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.info("trigger_action::exception %s %s %s",exc_type, exc_value, exc_traceback)
            pass

@tornado.gen.coroutine
def send_initial_data(client):
	try:
	    logging.info("send_initial_data::entering")
	    tconn = yield r.connect(DB_HOST,DB_PORT,DB_NAME)
	    #feed =  yield r.table("observations").pluck('sensorid','datetime','type','temp','measure_temp','pressure_sea','measure_pressure').order_by(r.desc('datetime')).limit(200).order_by(r.asc('datetime')).run(tconn)
	    feed =  yield r.table("observations").order_by(r.desc('timestamp')).limit(200).order_by(r.asc('timestamp')).run(tconn) 
            for document in feed:
            	client.write_message(document) 
	    tconn.close()
            logging.info("send_initial_data::leaving")
	except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.info("send_initial_data::exception %s %s %s",exc_type, exc_value, exc_traceback)
            pass


#send data updates to all clients who have suscribed
@tornado.gen.coroutine
def send_data_update():
    while True:
        try:
	    logging.info("send_data_update::trying to open database") 
            temp_conn = yield r.connect(DB_HOST,DB_PORT,DB_NAME)
	    logging.info("send_data_update::waiting for changes in observations table") 
	    feed = yield r.table("observations").changes().run(temp_conn)
	    logging.info("send_data_update::now pushing to clients") 
            while (yield feed.fetch_next()):
		data_update = yield feed.next()
                logging.info("send_data_update::received update - now looping clients") 
		for client in clients:
                        logging.info("send_data_update::writing to client::%s",data_update)
                 	client.write_message(data_update)
                logging.info("send_data_update::all clients notified")
            logging.info("send_data_update::closing connection") 
            temp_conn.close()
        except:
	    exc_type, exc_value, exc_traceback = sys.exc_info() 
	    logging.info("send_data_update::exception %s %s %s",exc_type, exc_value, exc_traceback)
            pass

if __name__ == "__main__":
	dbSetup()
	app = tornado.web.Application([(r'/', IndexHandler),(r'/ws', WSocketHandler)])
	#Start the server
    	server = tornado.httpserver.HTTPServer(app)
    	server.listen(options.port) #Bind port to server
    	tornado.ioloop.IOLoop.current().add_callback(send_data_update)
    	tornado.ioloop.IOLoop.instance().start()
