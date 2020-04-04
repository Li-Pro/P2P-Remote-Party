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
		rmt = input('Server address & port: ').split(' ')
		rmtaddr, rmtport = rmt[0], int(rmt[1]) # (int(x) for x in rmt.split(' '))
		# print((rmtaddr, rmtport))
	
	station = ClientStation()
	netst.joinParty(station, (rmtaddr, rmtport))
	
	while True:
		try:
			command = input('> ')
			if not command:
				continue
			
			if not command[0] == '/':
				netst.sendMsgToServer(station, bytes(command, 'utf-8'))
			
			else:
				cmd = command[1:]
				if cmd == 'leave':
					break
		
		except EOFError:
			break
		
		except Exception as e:
			print('Error occured, exiting.', type(e), e)
			break
	
	netst.leaveParty(station)
	
	return