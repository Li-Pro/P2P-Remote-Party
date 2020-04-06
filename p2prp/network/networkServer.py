import p2prp.network.networkStation as netst
import socket, threading, time

# Network Server
def recievePacket(station, ssock):
	while station.isServerOn:
		try:
			with ssock:
				sock = ssock.sock
				
				sock.settimeout(0.1)
				data = sock.recv(1024)
				
				if not data:
					break
				
				print('Recieved: "', str(''.join(map(chr, data))), '" from ', sock.getpeername())
		
		except netst.BLOCKING_EXCP:
			time.sleep(0.01)
			continue
		
		except Exception as e:
			print('recievePacket error: ', type(e), e)
			break
	
	if station.isServerOn:
		station.clientList.remove(ssock)
	
	print('Target <', sock.getpeername(),'> disconnected.')


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
					if not station.isServerOn:
						print('Blocking connectiong: server is off.')
						continue
					
					sconn = netst.SafeSocket(conn)
					station.clientList.add(sconn)
					
					station.addProcess(target=recievePacket, args=(station, sconn,))
	
	return

def startAuthorization(station):
	with station:
		station.addProcess(target=authorizeClients, args=(station,))
	
	return

def serverSendMsg(station, msg):
	cllist = {}
	with station:
		cllist = station.clientList
	
	for sclt in cllist:
		try:
			with sclt:
				clt = sclt.sock
				print('Sending "' + str(''.join(map(chr,msg))) + '" to: ', clt.getpeername())
				
				clt.settimeout(0.1)
				clt.send(msg)
		
		except netst.BLOCKING_EXCP:
			print('Sending time out.')
		
		except:
			print('Sending error.')
	
	return

def closeServer(station):
	print('Closing server.')
	
	with station:
		station.isServerOn = False
		subprocs = station.subproc.copy()
	
	for proc in subprocs:
		proc.join()
	
	station.sock.close()
	return