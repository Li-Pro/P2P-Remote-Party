import p2prp.network.networkStation as netst
import socket, threading, time

# Network Client
def recieveMsg(station):
	
	print('Thread started.')
	while station.isClientActive:
		try:
			with station:
				sock = station.sock
				
				sock.settimeout(0.1)
				data = sock.recv(1024)
				
				if not data:
					station.isClientActive = False
					break
				
				station.console.addLog('Recieved from server: ' + str(''.join(map(chr, data))))
				# print('Recieved from server: ', str(''.join(map(chr, data))))
		
		except netst.BLOCKING_EXCP:
			time.sleep(0.01)
			continue
		
		except Exception as e:
			print('Error during listening: ', type(e), e)
			break
	
	print('Server closed.')
	return

def joinParty(station, rmt):
	print('Connecting to: ', rmt[0], ':', rmt[1])
	
	# Error would stop client.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.connect(rmt)
		
		station.isClientActive = True
		station.addProcess(target=recieveMsg, args=(station,))
	
	return

def sendMsgToServer(station, msg):
	if not station.isClientActive:
		print('No active connection.')
		return
	
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
	if not station.isClientActive:
		print('No active connection.')
		return
	
	print('Disconnecting.')
	
	with station:
		station.isClientActive = False
	
	for proc in station.subproc:
		proc.join()
	
	station.sock.close()
	return