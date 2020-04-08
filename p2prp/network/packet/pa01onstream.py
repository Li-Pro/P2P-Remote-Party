from p2prp.network.packet import packetBase
import p2prp.util.utilStation as util

def printLog(station, *args):
	LOG_MARK = '[packetUtil]: '
	station.console.addLog(util.toStr(LOG_MARK, *args))

class PackA01OnStream(packetBase.S2CPacketBase):
	
	@staticmethod
	def getID():
		return 'a01'
	
	def fromBytes(self, buf):
		return self
	
	def toBytes(self, buf):
		return
	
	def clientHandlePacket(self, station, sock):
		with station:
			station.isStreaming = True
		
		printLog(station, 'Server is now streaming.')