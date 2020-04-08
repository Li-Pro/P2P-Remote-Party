import p2prp
import p2prp.network.networkServer as netst
import p2prp.ui.UIStation as guist
import p2prp.util.utilStation as util
import threading, requests

class ServerStation:
	def __init__(self, console):
		self.lock = threading.Lock()
		self.sock = None
		self.console = console
		
		self.clientList = set()
		self.subproc = []
		
		self.isServerOn = False
		self.isServerStreaming = False
	
	def addProcess(self, *args, **kwargs):
		nproc = threading.Thread(*args, **kwargs)
		self.subproc.append(nproc)
		nproc.start()
	
	def __enter__(self):
		self.lock.acquire()
	
	def __exit__(self, type, value, traceback):
		self.lock.release()

def printLog(station, *args):
	LOG_MARK = '[serverMain] '
	station.console.addLog(util.toStr(LOG_MARK, *args))

def runServer():
	print('Running P2PRP server.')
	netst.stationStartup()
	
	console = guist.hostConsole()
	station = ServerStation(console)
	
	root, logt, inp = console.root, console.logt, console.inp
	
	netst.hostParty(station)
	netst.startAuthorization(station)
	
	ext_ip = None
	def submitCommand(e):
		if not inp.get():
			return
		
		command = inp.get()
		
		try:
			if command[0] != '/':
				netst.serverSendRawMsg(station, bytes(command, 'utf-8'))
			
			else:
				cmds = command[1:].split(' ')
				opt = cmds[1:]
				cmd = cmds[0]
				
				if cmd == 'stop':
					root.destroy()
					return
				
				elif cmd == 'ip':
					nonlocal ext_ip
					
					if ext_ip == None:
						ext_ip = requests.get('https://api.ipify.org').text
					
					printLog(station, 'External ip: ', ext_ip)
				
				elif cmd == 'stream':
					# if not opt:
						# printLog(station, 'Server streaming is ' + ('ON' if station.isServerStreaming else 'OFF'))
					
					# else:
					if opt:
						stat = opt[0]
						if stat == 'on':
							netst.startStreaming(station, True)
						
						elif stat == 'off':
							netst.startStreaming(station, False)
					
					printLog(station, 'Server streaming is ' + ('ON' if station.isServerStreaming else 'OFF'))
		
		except Exception as e:
			print('Error occured, exiting.', type(e), e)
		
		logt.see('end')
		inp.delete(0, 'end')
		
		return
	
	root.bind('<Return>', submitCommand)
	root.bind('<Button-1>', lambda e: inp.focus_set())
	
	console.scheduleUpdate()
	root.mainloop()
	
	netst.closeServer(station)
	
	return