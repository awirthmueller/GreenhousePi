import os
import socket

HOSTNAME = socket.gethostname()

DB_HOST = os.environ.get('DB_HOST') or "0.0.0.0"
DB_PORT = os.environ.get('DB_PORT') or 28015
DB_NAME = "greenhouse_pi"
PROJECT_TABLE = 'observations'
