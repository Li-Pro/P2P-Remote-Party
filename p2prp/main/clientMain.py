import p2prp
import p2prp.network.networkClient as netst
import p2prp.ui.UIStation as guist
import threading

class ClientStation:
	def __init__(self):
		self.lock = threading.Lock()
		self.sock = None
		
		self.subproc = []
		
		self.isClientActive = False
	
	def addProcess(self, *args, **kwargs):
		nproc = threading.Thread(*args, **kwargs)
		self.subproc.append(nproc)
		nproc.start()
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.lock.release()

def runClient(rmtaddr=None, rmtport=None):
	print('Running P2PRP client.')
	
	console = guist.hostConsole()
	root, logt, inp = console.root, console.logt, console.inp
	
	def submitCommand(e):
		if not inp.get():
			return
		
		logt.configure(state='normal')
		logt.insert('end', inp.get() + '\n')
		logt.configure(state='disabled')
		inp.delete(0, 'end')
		
		return
	
	root.bind('<Return>', submitCommand)
	root.mainloop()
	
	if rmtaddr == None:
		rmt = input('Server address & port: ').split(' ')
		rmtaddr, rmtport = rmt[0], int(rmt[1])
	
	station = ClientStation()
	netst.joinParty(station, (rmtaddr, rmtport))
	
	while station.isClientActive:
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