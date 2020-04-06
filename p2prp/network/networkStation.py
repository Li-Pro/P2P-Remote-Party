# import p2prp
import socket, threading, time

BLOCKING_EXCP = (BlockingIOError, socket.timeout)

# Common Server
class SafeSocket:
	def __init__(self, sock):
		self.sklock = threading.Lock()
		self.sock = sock
	
	def __enter__(self):
		self.sklock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.sklock.release()

def scheduleTimeout(sock, func, args=(), sctime=0.1, scintv=0.01):
	rep = None
	try:
		sock.settimeout(sctime)
		rep = func(*args)
	
	except BLOCKING_EXCP as e:
		time.sleep(scintv)
		rep = e
	
	# except BlockingIOError as e:
		# time.sleep(scintv)
		# rep = e
	
	# except socket.timeout as e:
		# time.sleep(scintv)
		# rep = e
	
	return rep