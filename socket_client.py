import socket

HOST='127.0.0.1'
PORT=9000

for counter in range (5):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.sendall(b'This is the message')
		data = s.recv(256)
		print(data)
		data_ascii = data.decode("ascii")
		print ("data_ascii: ", data_ascii)
	print('Received back from server:', data_ascii)
	print('')