import p2prp
import p2prp.network.networkServer as netst
import threading

class ServerStation:
	def __init__(self):
		self.lock = threading.Lock()
		self.sock = None
		self.clientList = []
		self.subproc = []
		
		self.isServerOn = True
	
	def addProcess(self, *args, **kwargs):
		nproc = threading.Thread(*args, **kwargs)
		self.subproc.append(nproc)
		nproc.start()
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.lock.release()

def runServer():
	print('Running P2PRP server.')
	
	station = ServerStation()
	
	netst.hostParty(station)
	netst.startAuthorization(station)
	
	ext_ip = None
	while True:
		try:
			command = input('> ')
			if not command:
				continue
			
			if command[0] != '/':
				netst.serverSendMsg(station, bytes(command, 'utf-8'))
			
			else:
				cmd = command[1:]
				if cmd == 'stop':
					break
				
				elif cmd == 'ip':
					import requests
					if ext_ip == None:
						ext_ip = requests.get('https://api.ipify.org').text
					
					print('External ip: ', ext_ip)
		
		except EOFError:
			break
		
		except Exception as e:
			print('Error occured, terminating server: ', type(e), e)
			break
	
	netst.closeServer(station)
	
	return