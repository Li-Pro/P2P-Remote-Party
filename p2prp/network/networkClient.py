import p2prp.network.networkStation as netst
import p2prp.util.utilStation as util
import p2prp.ui.UIStation as guist
from p2prp.network.packet import packetBase as pkbase, packets as packs

import socket, threading, time

def printLog(station, *args):
	LOG_MARK = '[networkClient]'
	station.console.addLog(util.toStr(LOG_MARK, *args))

# Network Client
def receiveMsg(station):
	
	while station.isClientActive:
		try:
			with station:
				sock = station.sock
				
				data = netst.recvPack(sock)
				
				if not data:
					station.isClientActive = False
					break
			
			data.clientHandlePacket(station, sock)
		
		except netst.BLOCKING_EXCP:
			time.sleep(0.01)
			continue
		
		except Exception as e:
			print('Error during listening: ', type(e), e)
			break
	
	printLog(station, 'Connection closed.')
	return

def joinParty(station, rmt):
	
	# Error would stop client.
	with station:
		printLog(station, 'Connecting to: ', rmt[0], ':', rmt[1])
		sock = socket.socket()
		station.sock = sock
		
		sock.connect(rmt)
		
		station.isClientActive = True
		station.addProcess(target=receiveMsg, args=(station,))
	
	return

def closeStream(station):
	with station:
		station.streamWindow.withdraw()
	
	return

def openStream(station):
	with station:
		station.streamWindow.deiconify()
	
	return

def sendMsgToServer(station, pack):
	if not station.isClientActive:
		print('No active connection.')
		return
	
	with station:
		sock = station.sock
		
		try:
			netst.sendPack(sock, pack)
		
		except BlockingIOError as e:
			print('Sending time out.')
		
		except socket.timeout as e:
			print('Sending time out.')
		
		except Exception as e:
			print('Sending error: ', type(e), e)
	
	return

def sendRawMsgToServer(station, msg):
	printLog(station, 'Sending "' + msg.decode('utf-8') + '" to server.')
	sendMsgToServer(station, packs.PackA03RawMsg(msg))

def leaveParty(station):
	if not station.isClientActive:
		print('No active connection.')
		return
	
	printLog(station, 'Disconnecting.')
	
	with station:
		station.isClientActive = False
	
	for proc in station.subproc:
		proc.join()
	
	station.sock.close()
	return

def stationStartup():
	pkbase.registerPackets()