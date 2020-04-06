# import p2prp
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

def recievePacket(station, sock):
	# sock = conn NOT station.sock
	while station.isServerOn:
		try:
			def recPack(sock):
				data = sock.recv(1024)
				if not data:
					return data
				
				return data
			
			data = scheduleTimeout(sock, recPack, (sock,))
			if isinstance(data, Exception):
				continue
			
			# print('# Recieved: "', data, '" from ', sock.getpeername())
			
			if not data:
				break
			print('Recieved: "', data, '" from ', sock.getpeername())
		
		except Exception as e:
			print('recievePacket error: ', type(e), e)
			break
	
	# Remove client / server here
	print('Target <', sock.getpeername(),'> disconnected.')
