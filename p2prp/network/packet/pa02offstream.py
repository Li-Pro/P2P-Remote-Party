from p2prp.network.packet import packetBase
import p2prp.util.utilStation as util

def printLog(station, *args):
	LOG_MARK = '[packetUtil]: '
	station.console.addLog(util.toStr(LOG_MARK, *args))

class PackA02OffStream(packetBase.S2CPacketBase):
	
	@staticmethod
	def getID():
		return 'a02'
	
	def fromBytes(self, buf):
		return self
	
	def toBytes(self, buf):
		return
	
	def clientHandlePacket(self, station, sock):
		with station:
			station.isStreaming = False
		
		printLog(station, 'Server is now off-streaming.')