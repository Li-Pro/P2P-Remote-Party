import p2prp
import socket, threading, time

# Common Server
def scheduleTimeout(sock, func, args=(), sctime=0.1, scintv=0.01):
	
	rep = None
	try:
		sock.settimeout(0.1)
		rep = func(*args)
	
	except BlockingIOError as e:
		time.sleep(0.01)
		rep = e
	
	except socket.timeout as e:
		time.sleep(0.01)
		rep = e
	
	return rep

# sock = conn NOT station.sock
def recievePacket(station, sock):
	
	while station.isServerOn:
		
		#time.sleep(0.01)
		# print('recLOoopp')
		try:
			def recPack(sock):
				data = sock.recv(1024)
				if not data:
					return data
				
				return data
			
			data = scheduleTimeout(sock, recPack, (sock,))
			if isinstance(data, Exception):
				continue
			
			print('# Recieved: "', data, '" from ', sock.getpeername())
			
			if not data:
				break
			print('Recieved: "', data, '" from ', sock.getpeername())
		
		except Exception as e:
			print('recievePacket error: ', type(e), e)
			break
	
	# Remove client / server here
	print('Target <', sock.getpeername(),'> disconnected.')

# Network Server
def hostParty(station):
	print('Hosting party.')
	
	# Error hosting will stop server.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.bind(('', 0))
		sock.listen()
		print('Opening at: ', socket.gethostbyname(socket.gethostname()), ':', sock.getsockname()[1])
	
	return

def authorizeClients(station):
	print('Starting authorization.')
	
	with station:
		sock = station.sock
	
	while station.isServerOn:
			# print('autLOoopp')
			# time.sleep(0.01)
			
			try:
				def acpPack(station, sock):
					with station:
						return sock.accept()
				
				rep = scheduleTimeout(sock, acpPack, (station, sock,))
				if isinstance(rep, Exception):
					continue
				
				conn, addr = rep
			
			except Exception as e:
				print('Authorization error: ', type(e), e)
				break
			
			else:
				print('Accepted connection from: ', addr)
				with station:
					station.clientList.append(conn)
					clt_thr = threading.Thread(target=recievePacket, args=(station, conn,))
					station.subproc.append(clt_thr)
					clt_thr.start()
	
	print('Thread auth stopped.')
	return

def startAuthorization(station):
	with station:
		auth_thr = threading.Thread(target=authorizeClients, args=(station,))
		station.subproc.append(auth_thr)
		auth_thr.start()
	
	return

def serverSendMsg(station, msg):
	
	with station:
		for clt in station.clientList:
			print('Sending "' + str(''.join(map(chr,msg))) + '" to: ', clt.getpeername())
			
			try:
				clt.settimeout(0.1)
				clt.send(msg)
			
			except BlockingIOError as e:
				print('Sending time out.')
			
			except socket.timeout as e:
				print('Sending time out.')
			
			except:
				print('Sending error.')
	
	return

def closeServer(station):
	print('Closing server.')
	
	with station:
		# # print('A')
		# # station.sock.close()
		# # station.isServerOn = False
		
		# # print('B')
		subprocs = station.subproc.copy()
		# clts = station.clientList.copy()
	
	station.isServerOn = False
	
	print('Now closed.')
	for proc in subprocs:
		# print('Waiting for: ', proc, proc.target)
		# proc.join()
		proc.join()
	
	# for clt in clts:
	# serverSendMsg(station, bytes('Server closing.', 'utf-8'))
		
		# station.clientList.clear()
	
	return

# Network Client
def joinParty(station, rmt):
	print('Connecting to: ', rmt[0], ':', rmt[1])
	
	# Error would stop client.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.connect(rmt)
		# sock.listen()
	
	return

def sendMsgToServer(station, msg):
	
	with station:
		sock = station.sock
		print('Sending "' + str(''.join(map(chr,msg))) + '" to server: ', sock.getpeername())
		
		try:
			sock.settimeout(0.1)
			sock.send(msg)
		
		except BlockingIOError as e:
			print('Sending time out.')
		
		except socket.timeout as e:
			print('Sending time out.')
		
		except:
			print('Sending error.')
	
	return

def leaveParty(station):
	print('Disconnecting.')
	
	with station:
		station.sock.close()
	
	return