import socket
import threading

HOST='0.0.0.0'
PORT=9000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(1)

connections=[]

def handler(connectFrom, address):
	global connections

	while True:
		data = connectFrom.recv(256)
		print(data.decode("ascii"),end='')
		for connection in connections:
			connection.send(bytes("The data received was: ", encoding='utf8') + bytes(data))
		if not data:
			connections.remove(connection)
			close.connection()
			break


try:
	while True:
		connectFrom, address = sock.accept()
		cThread = threading.Thread(target=handler, args=(connectFrom, address))
		cThread.daemon=True
		cThread.start()
		connections.append(connectFrom)
		for connection in connections: print(connection)
except:
	print("An error occured")

finally:
	print("Cleaning up")
	sock.close()