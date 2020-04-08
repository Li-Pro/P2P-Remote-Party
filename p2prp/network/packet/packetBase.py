import io
from abc import ABC, abstractmethod, abstractclassmethod, abstractstaticmethod

from p2prp.network.packet import pa01onstream, pa02offstream, pa03rawmsg

# Base header: 10-bytes(at least)

# PACK_REG = {'a01': pa01onstream, 'a02': pa02offstream, 'a03': pa03rawmsg}
PACK_REG = {}
REG_PCLASS = [pa03rawmsg] # [pa01onstream, pa02offstream, pa03rawmsg]

class PacketBase(ABC):
	def decode(self, data):
		buf = io.BytesIO(data)
		
		header = buf.read(10)
		pack_id = int(header)
		
		if not pack_id in PACK_REG:
			return None
		
		pack_cls = PACK_REG[pack_id]
		return pack_cls().fromBytes(buf)
	
	def encode(self):
		buf = io.BytesIO()
		data = self.toBytes(buf)
		return buf.getvalue()
	
	@abstractclassmethod
	def getID():
		pass
	
	@abstractmethod
	def fromBytes(self, buf):
		pass
	
	@abstractmethod
	def toBytes(self, buf):
		pass
	
	@abstractmethod
	def clientHandlePacket(self, station):
		pass
	
	@abstractmethod
	def serverHandlePacket(self, station):
		pass

class ClientPacketBase(PacketBase):
	def serverHandlePacket(self, station):
		raise Exception('Client received server-side packet: ', type(self))

class ServerPacketBase(PacketBase):
	def clientHandlePacket(self, station):
		raise Exception('Server received client-side packet: ', type(self))

def registerPackets():
	for cls in REG_PCLASS:
		assert (not cls in PACK_REG)
		PACK_REG[cls.getID()] = cls