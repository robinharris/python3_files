import socket

HOST='127.0.0.1'
PORT=9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen(1)
	counter = 0
	element = [counter]

	while True:
		conn, addr = s.accept()
		counter += 1
		element[0] = counter
		byteArray = bytearray(element)
		with conn:
			print('Connected by: ', addr[0])
			while True:
				data = conn.recv(256)
				if not data: break
				data_ascii = data.decode("ascii")
				print('Data received from client: ', data.decode("ascii"))
				conn.sendall(byteArray)
