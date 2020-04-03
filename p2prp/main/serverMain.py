import p2prp
import p2prp.network.networkStation as netst
import threading

class ServerStation:
	def __init__(self):
		self.lock = threading.Lock()
		self.sock = None
		self.clientList = []
		self.subproc = []
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.lock.release()

def runServer():
	print('Running P2PRP server.')
	
	station = ServerStation()
	
	netst.hostParty(station)
	netst.startAuthorization(station)
	
	# Start local server
	# p2prp.runClient(station.sock.getsockname())
	# loccrt_thr = threading.Thread(target=p2prp.runClient, args=(station.sock.getsockname(),))
	# loccrt_thr.start()
	
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
		
		except:
			print('Error occured, terminating server.')
			break
	
	netst.closeServer(station)
	
	return

def main():
	return

if __name__=="__main__":
	main()