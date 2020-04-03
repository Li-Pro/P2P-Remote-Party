import p2prp
import p2prp.network.networkStation as netst
import threading

class ServerStation:
	def __init__(self):
		self.lock = threading.Lock()
		self.sock = None
		self.clientList = []
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self):
		self.lock.release()

def runServer():
	print('Running P2PRP server.')
	
	station = ServerStation()
	
	netst.hostParty(station)
	netst.startAuthorization(station)
	
	while True:
		command = input('> ')
		if not command:
			continue
		
		if command[0] != '/':
			netst.serverSendMsg(station, command)
		else:
			cmd = command[1:]
			if cmd == 'stop':
				break
	
	netst.closeServer(station)
	
	return

def main():
	return

if __name__=="__main__":
	main()