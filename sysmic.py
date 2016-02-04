#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys, os, socket
import time as timer
import random

if sys.platform.startswith('linux'):
	os.system('clear')
elif sys.platform.startswith('win'):
	os.system('cls')

hostname="127.0.0.1"
port=6969
max_clients=7
version_Check="0.1"
#rango
r=1

def init():
	sc,addr=getCliente()
	infoCliente(sc,addr)

def getDato():
	return sc.recv(1024)

def getCliente():
	sc, addr = s.accept()
	return sc, addr

def infoCliente(sock,dirIp):
	print "Cliente conectado desde",dirIp
	print "Nombre del Cliente:",sock.recv(1024)
	sock.sendall("Getversion")
	clientVersion=getDato()
	if clientVersion==version_Check:
		print "Version del cliente:",clientVersion
		sock.sendall("hostname")
	else:
		print "Version del cliente: desconocida, es necesaria la actualizacion."
		sock.sendall("update")
	print ""

def goSleep(seg):
	#print "Esperando",seg,"segundos..."
	timer.sleep(seg)

def getRange():
	rango=random.randrange(2, 8, 1)
	return rango

def setTemp(t):
	temp=t * int(getRange()*327.5)
	print "Temperatura...",temp
	sc.sendall("Temperatura")
	sc.sendall(str(temp))

def setGas(g):
	gas=g * int(getRange()*25.8)
	print "Gases...",gas
	sc.sendall("Gases")
	sc.sendall(str(gas))

def setPresion(p):
	pres=p * int(getRange()*3.35)
	print "Presion...",pres
	sc.sendall("Presion")
	sc.sendall(str(pres))

def setHumedad(h):
	hum=h * int(getRange()*5.75)
	print "Humedad...",hum
	sc.sendall("Humedad")
	sc.sendall(str(hum))

def setParticulas(p):
	part=p * int(getRange()*12.1)
	print "Particulas...",part
	sc.sendall("Particulas")
	sc.sendall(str(part))

def setLava(l):
	lava=l * int(getRange()*7.5)
	print "Lava...",lava
	sc.sendall("Lava")
	sc.sendall(str(lava))

def mainloop():
#Main Loop
	print "Enviando estadisticas..."
	while True:
		r=getRange()
		#print "random es",r
		if int(r)==2:
			setTemp(r)
		elif int(r)==3:
				setGas(r)
		elif int(r)==4:
			setLava(r)
		elif int(r)==5:
			setHumedad(r)
		elif int(r)==6:
			setParticulas(r)
		elif int(r)==7:
			setPresion(r)
		goSleep(r)

#Main App
try:
	s = socket.socket()
	#hostname= socket.gethostname()
	s.bind((hostname, port))
	s.listen(max_clients)
	print "Bienvenido al server",hostname
	print "Esperando conexiones..."
	print ""

	sc,addr=getCliente()
	infoCliente(sc,addr)
	mainloop()
except socket.error, msg:
	print "Ocurrio un error al Ejecutar el servidor...",hostname

sc.close()
s.close()
print "conexion servidor cerrada."
