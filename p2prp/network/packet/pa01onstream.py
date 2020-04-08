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
		import p2prp.network.networkClient as netst
		
		with station:
			station.isStreaming = True
		
		netst.openStream(station)
		printLog(station, 'Server is now streaming.')