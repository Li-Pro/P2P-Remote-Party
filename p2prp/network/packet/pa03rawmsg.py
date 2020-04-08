from p2prp.network.packet import packetBase
import p2prp.util.utilStation as util

def printLog(station, *args):
	station.console.addLog(util.toStr(*args))

class PackA03RawMsg(packetBase.PacketBase):
	def __init__(self, msg=b''):
		self.msg = msg
	
	@staticmethod
	def getID():
		return 'a03'
	
	def fromBytes(self, buf):
		self.msg = buf.read()
		return self
	
	def toBytes(self, buf):
		buf.write(self.msg)
	
	def clientHandlePacket(self, station, sock):
		printLog(station, 'Received from server: ', self.msg.decode('utf-8'))
	
	def serverHandlePacket(self, station, sock):
		# print('Handling: ', self.msg)
		printLog(station, 'Received from client: ', self.msg.decode('utf-8'))