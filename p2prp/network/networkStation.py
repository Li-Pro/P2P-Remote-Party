import p2prp
import socket, threading

# Network Server
def hostParty(station):
	print('Hosting party.')
	
	# Error hosting will stop server.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.bind(('', 0))
		#sock.listen(1)
		sock.listen()
		print('Opening at: ', socket.gethostbyname(socket.gethostname()), ':', sock.getsockname()[1])
	
	return

def authorizeClients(station):
	print('Starting authorization.')
	
	sock = station.sock
	while True:
		try:
			conn, addr = sock.accept()
		except:
			break
		else:
			print('Accepted connection from: ', addr)
			with station:
				station.clientList.append(conn)
	
	return

def startAuthorization(station):
	auth_thr = threading.Thread(target=authorizeClients, args=(station,))
	station.subproc.append(auth_thr)
	auth_thr.start()
	return

def serverSendMsg(station, msg):
	# print('Sending Msg: ', msg)
	
	for clt in station.clientList:
		print('Sending "' + str(''.join(map(chr,msg))) + '" to: ', clt.getpeername())
		try:
			clt.send(msg)
		except:
			pass
	
	return

def closeServer(station):
	print('Closing server.')
	
	with station:
		
		station.sock.close()
		for proc in station.subproc:
			proc.join()
		
		for clts in station.clientList:
			serverSendMsg(station, bytes('Server closing.', 'utf-8'))
		
		# station.clientList.clear()
	
	return

# Network Client
def joinParty(station):
	return

def leaveParty(station):
	return