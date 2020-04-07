import p2prp
import p2prp.network.networkClient as netst
import p2prp.ui.UIStation as guist
import threading

class ClientStation:
	def __init__(self, console):
		self.lock = threading.Lock()
		self.sock = None
		self.console = console
		
		self.subproc = []
		
		self.isClientActive = False
	
	def renew(self, console):
		self.__init__(console)
	
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
	station = ClientStation(console)
	
	root, logt, inp = console.root, console.logt, console.inp
	
	def submitCommand(e):
		if not inp.get():
			return
		
		command = inp.get()
		
		try:
			if not command[0] == '/':
				# logt.configure(state='normal')
				# logt.insert('end', inp.get() + '\n')
				# logt.configure(state='disabled')
				
				console.addLog(inp.get())
				netst.sendMsgToServer(station, bytes(command, 'utf-8'))
			
			else:
				cmds = command[1:].split(' ')
				opt = cmds[1:]
				cmd = cmds[0]
				
				if cmd == 'leave':
					netst.leaveParty(station)
				
				elif cmd == 'join':
					assert (len(opt) >= 2)
					
					if station.isClientActive:
						print('Already in connection.')
						return
					
					station.renew(console)
					rmtaddr, rmtport = opt[0], int(opt[1])
					netst.joinParty(station, (rmtaddr, rmtport))
				
				elif cmd == 'stop':
					station.console.root.destroy()
					return
				
				else:
					pass
		
		except Exception as e:
			print('Error occured, exiting.', type(e), e)
			return
		
		logt.see('end')
		inp.delete(0, 'end')
		
		return
	
	root.bind('<Return>', submitCommand)
	root.bind('<Button-1>', lambda e: inp.focus_set())
	
	console.scheduleUpdate()
	root.mainloop()
	
	if station.isClientActive:
		netst.leaveParty(station)
	
	return