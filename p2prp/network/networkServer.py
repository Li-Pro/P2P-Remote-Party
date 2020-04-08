import p2prp.network.networkStation as netst
import p2prp.util.utilStation as util
from p2prp.network.packet import packetBase as pkbase, packets as packs

import socket, threading, time

def printLog(station, *args):
	LOG_MARK = '[networkServer] '
	station.console.addLog(util.toStr(LOG_MARK, *args))

# Network Server
def recievePacket(station, ssock):
	while station.isServerOn:
		try:
			with ssock:
				sock = ssock.sock
				
				data = netst.recvPack(sock)
				
				if not data:
					break
				
				data.serverHandlePacket(station, sock)
		
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

def serverSendMsg(station, pack):
	cllist = {}
	with station:
		cllist = station.clientList
	
	for sclt in cllist:
		try:
			with sclt:
				clt = sclt.sock
				
				netst.sendPack(clt, pack)
		
		except netst.BLOCKING_EXCP:
			print('Sending time out.')
		
		except Exception as e:
			print('Sending error: ', type(e), e)
	
	return

def serverSendRawMsg(station, msg):
	printLog(station, 'Posting "' + msg.decode('utf-8') + '".')
	serverSendMsg(station, packs.PackA03RawMsg(msg))

def startStreaming(station, isStreaming):
	if station.isServerStreaming == isStreaming:
		return
	
	# print('Trying to acquire lock.')
	with station:
		# print('Lock acquired.')
		station.isServerStreaming = isStreaming
	
	if isStreaming:
		serverSendMsg(station, packs.PackA01OnStream())
	else:
		serverSendMsg(station, packs.PackA02OffStream())
	
	# print('Finishing.')
	

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
	pkbase.registerPackets()