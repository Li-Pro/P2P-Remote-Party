import p2prp.network.packet.packetBase as pkbase
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
	
	return rep

def sendPack(sock, pack):
	data = pkbase.encode(pack)
	
	datlen = len(data)
	totalSent = 0
	while totalSent < datlen:
		nsent = sock.send(data[totalSent:])
		if not nsent:
			raise Exception('Sending error: connection has broken.')
		
		totalSent += nsent

def recvPack(sock):
	sock.settimeout(0.01)
	data = sock.recv(15)
	if not data:
		return data
	
	pack_len = int(data[:10])
	
	while len(data) < pack_len:
		ndat = sock.recv(1024)
		if not ndat:
			raise Exception('Receiving error: connection has broken.')
		
		data += ndat
	
	return pkbase.decode(data)

def stationStartup():
	pkbase.registerPackets()