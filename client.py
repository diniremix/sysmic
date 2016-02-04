#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import socket,os,sys

if sys.platform.startswith('linux'):
	os.system('clear')
elif sys.platform.startswith('win'):
	os.system('cls')

def getDato(sock):
	return sock.recv(1024)

hostname="localhost"
port=6969
app_version="0.1"
print "Sysmic Version",app_version
usuario=raw_input("Nombre de usuario: ")


try:
	s = socket.socket()
	print ""
	print "Conectandose a: "+hostname+":"+str(port)+"..."
	s.connect((hostname,port))
	s.send(usuario)

	recibido=getDato(s)
	if recibido=="Getversion":
		s.send(app_version)

	serverName=getDato(s)
	if serverName=="update":
		print "Esta version del cliente necesita una actualizacion."
		sys.exit(1)
	else:
		print "Conexion establecida con el servidor",serverName
		print "Obteniendo estadisticas de",serverName
		print ""
	i=0
	#Main loop
	while True:
		recibido = getDato(s)
		#No se esta recibiendo datos...
		if not recibido:
			i=i+1
			if i>10:
				break
		elif recibido=="Temperatura":
			print 'Recibiendo Temperatura...'
			recibido = getDato(s)
			if int(recibido)>500:
				print "Registro de Temperatura Elevada:",recibido,"grados"
		elif recibido=="Gases":
			print 'Recibiendo Gases...'
			recibido = getDato(s)
			if int(recibido)>1500:
				print "Registro de Gases Elevado:",recibido,"Mt3"
		elif recibido=="Lava":
			print 'Recibiendo Lava...'
			recibido = getDato(s)
			if int(recibido)>500:
				print "Registro de Lava Elevado:",recibido,"Mt2"
		elif recibido=="Humedad":
			print 'Recibiendo Humedad...'
			recibido = getDato(s)
			if int(recibido)>700:
				print "Registro de Humedad Elevada:",recibido,"Hg3"
		elif recibido=="Particulas":
			print 'Recibiendo Particulas...'
			recibido = getDato(s)
			if int(recibido)>2000:
				print "Registro de Particulas Elevada:",recibido,"Mt2"
		elif recibido=="Presion":
			print 'Recibiendo Presion...'
			recibido = getDato(s)
			if int(recibido)>1700:
				print "Registro de Presion Elevado:",recibido,"Mt3"
		if not recibido=="":
			print recibido

except socket.error, msg:
	print "Ocurrio un error al conectarse al servidor..."
s.close()
print "Conexion cliente cerrada."
