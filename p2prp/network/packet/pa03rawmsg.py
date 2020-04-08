from p2prp.network.packet import packetBase

class PackA03RawMsg(packetBase.PacketBase):
	def __init__(self, msg):
		self.msg = msg
	
	@staticmethod
	def getID():
		return 'a03'
	
	def fromBytes(self, buf):
		# msglen = int(buf.read(10))
		self.msg = buf.getvalue() # buf.read(msglen)
	
	def toBytes(self, buf):
		# buf.write(bytes('{:<10}'.format(len(self.msg)), 'utf-8'))
		buf.write(self.msg)
	
	def clientHandlePacket(self, station):
		station.console.addLog(self.msg)
	
	def serverHandlePacket(self, station):
		station.console.addLog(self.msg)