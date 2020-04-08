import io
from abc import ABC, abstractmethod, abstractclassmethod, abstractstaticmethod

# Base header: 15-bytes(at least)

PACK_REG = {}

class PacketBase(ABC):
	@abstractstaticmethod
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

def decode(data):
	buf = io.BytesIO(data)
	
	header = buf.read(15)
	pack_len = int(header[:10])
	pack_id = header[10:].decode('utf-8').strip()
	
	if not pack_id in PACK_REG:
		print('Receiving: <', pack_id, '>, which is not recognize in this side.')
		return None
	
	pack_cls = PACK_REG[pack_id]
	# print('Decoding type: ', pack_cls)
	return pack_cls().fromBytes(buf)

def encode(pack):
	buf = io.BytesIO()
	pack.toBytes(buf)
	
	data = buf.getvalue()
	
	pack_len = 15 + len(data)
	assert( len(str(pack_len)) <= 10 )
	
	pack_id = pack.getID()
	header = bytes('{:<10}{:<5}'.format(pack_len, pack_id), 'utf-8')
	
	return header + data

def registerPackets():
	import p2prp.network.packet.packets as packs
	
	REG_PCLASS = [packs.PackA03RawMsg] # [pa01onstream, pa02offstream, pa03rawmsg]
	
	global PACK_REG
	
	for cls in REG_PCLASS:
		assert (not cls in PACK_REG)
		PACK_REG[cls.getID()] = cls