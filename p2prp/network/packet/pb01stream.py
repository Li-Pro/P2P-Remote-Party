from p2prp.network.packet import packetBase as pkbase
import pyautogui as pagui

class PackB01Stream(pkbase.S2CPacketBase):
	
	def __init__(self, size=(0,0), data=b''):
		self.size = size
		self.data = data
		
		# print('Data: ', size, len(data))
	
	@staticmethod
	def getID():
		return 'b01'
	
	def fromBytes(self, buf):
		self.size = int(buf.read(5)), int(buf.read(5))
		self.data = buf.read()
		return self
	
	def toBytes(self, buf):
		buf.write(bytes('{:<5}{:<5}'.format(*self.size), 'utf-8'))
		buf.write(self.data)
		return
	
	def clientHandlePacket(self, station, sock):
		station.streamWindow.setImage(self.size, self.data)
		
		# print('Receiving stream: ', self.size, len(self.data))