import p2prp
import networkStation as net

clientList = []

def runServer():
	print('Running P2PRP server.')
	
	sock = net.hostParty()
	net.startAuthorization(sock, clientList)
	
	while True:
		command = input('> ')
		if command == '/stop':
			break
	
	closeServer(sock, clientList)
	
	return

def main():
	return

if __name__=="__main__":
	main()