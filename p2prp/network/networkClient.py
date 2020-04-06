import p2prp.network.networkStation as netst
import socket, threading, time

# Network Client
def joinParty(station, rmt):
	print('Connecting to: ', rmt[0], ':', rmt[1])
	
	# Error would stop client.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.connect(rmt)
	
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