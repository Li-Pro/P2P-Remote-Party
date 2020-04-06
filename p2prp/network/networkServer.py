import p2prp.network.networkStation as netst
import socket, threading, time

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
			try:
				def acpPack(station, sock):
					with station:
						return sock.accept()
				
				rep = netst.scheduleTimeout(sock, acpPack, (station, sock,))
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
					clt_thr = threading.Thread(target=netst.recievePacket, args=(station, conn,))
					station.subproc.append(clt_thr)
					clt_thr.start()
	
	# print('Thread auth stopped.')
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
		station.isServerOn = False
		subprocs = station.subproc.copy()
	
	print('Now closed.')
	for proc in subprocs:
		proc.join()
	
	station.sock.close()
	# station.clientList.clear()
	return