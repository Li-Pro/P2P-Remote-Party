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
	
	# except Exception as e:
		# print('Exception during timeout: ', type(e), e)
	
	return rep

def recievePacket(sock):
	
	while True:
		try:
			# sock.settimeout(0.1)
			def recPack(sock):
				data = sock.recv(1024)
				if not data:
					return data
				
				return data
			
			data = scheduleTimeout(sock, recPack, (sock,))
			if isinstance(data, Exception):
				continue
			
			if not data:
				break
			print('Recieved: "', data, '" from ', sock.getpeername())
			
		# except BlockingIOError:
			# time.sleep(0.01)
			# continue
		
		# except socket.timeout:
			# time.sleep(0.01)
			# continue
		
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
	
	sock = station.sock
	while True:
		try:
			# sock.settimeout(0)
			def acpPack(sock):
				return sock.accept()
			# conn.setblocking(False)
			
			rep = scheduleTimeout(sock, acpPack, (sock,))
			if isinstance(rep, Exception):
				continue
			
			conn, addr = rep
		
		# except BlockingIOError:
			# time.sleep(0.01)
			# continue
		
		# except socket.timeout:
			# time.sleep(0.01)
			# continue
		
		except Exception as e:
			print('Authorization error: ', type(e), e)
			break
		# except:
			# break
		
		else:
			print('Accepted connection from: ', addr)
			with station:
				station.clientList.append(conn)
				clt_thr = threading.Thread(target=recievePacket, args=(conn,))
				station.subproc.append(clt_thr)
				clt_thr.start()
	
	return

def startAuthorization(station):
	auth_thr = threading.Thread(target=authorizeClients, args=(station,))
	station.subproc.append(auth_thr)
	auth_thr.start()
	return

def serverSendMsg(station, msg):
	for clt in station.clientList:
		print('Sending "' + str(''.join(map(chr,msg))) + '" to: ', clt.getpeername())
		
		with clt:
			try:
				clt.settimeout(0.1)
				clt.send(msg)
			
			except socket.timeout as e:
				print('Sending time out.')
			
			except:
				print('Sending error.')
	
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
def joinParty(station, rmt):
	print('Connecting to: ', rmt[0], ':', rmt[1])
	
	# Error would stop client.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.connect(rmt)
		sock.listen()
	
	return

def leaveParty(station):
	return