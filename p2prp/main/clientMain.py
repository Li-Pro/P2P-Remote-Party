import p2prp
import p2prp.network.networkStation as netst
import threading

class ClientStation:
	
	def __init__(self):
		self.lock = threading.Lock()
		self.sock = None
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.lock.release()

def runClient(rmtaddr=None, rmtport=None):
	print('Running P2PRP client.')
	
	if rmtaddr == None:
		rmt = input('Server address & port: ')
		rmtaddr, rmtport = rmt.split(' ')
		# print((rmtaddr, rmtport))
	
	station = ClientStation()
	netst.joinParty(station, (rmtaddr, rmtport))
	
	while True:
		try:
			command = input('> ')
			if command == '/leave':
				break
		
		except EOFError:
			break
		
		except:
			print('Error occured, exiting.')
			break
	
	netst.leaveParty(station)
	
	return