import p2prp.network.networkStation as netst
import p2prp.util.utilStation as util
from p2prp.network.packet import packetBase

import socket, threading, time

LOG_MARK = '[networkServer] '

def printLog(station, *args):
	station.console.addLog(util.toStr(LOG_MARK, *args))

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
				
				printLog(station, 'Recieved: "', data.decode('utf-8'), '" from ', sock.getpeername())
		
		except netst.BLOCKING_EXCP:
			time.sleep(0.01)
			continue
		
		except Exception as e:
			print('recievePacket error: ', type(e), e)
			break
	
	if station.isServerOn:
		station.clientList.remove(ssock)
	
	printLog(station, 'Target <', sock.getpeername(),'> disconnected.')


def hostParty(station):
	printLog(station, 'Hosting party.')
	
	# Error hosting will stop server.
	with station:
		sock = socket.socket()
		station.sock = sock
		
		sock.bind(('', 0))
		sock.listen()
		
		station.isServerOn = True
		printLog(station, 'Opening at: ', socket.gethostbyname(socket.gethostname()), ':', sock.getsockname()[1])
	
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
				printLog(station, 'Accepted connection from: ', addr)
				with station:
					if not station.isServerOn:
						printLog(station, 'Blocking connectiong: server is off.')
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
				printLog(station, 'Sending "' + msg.decode('utf-8') + '" to: ', clt.getpeername())
				
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

def stationStartup():
	packetBase.registerPackets()