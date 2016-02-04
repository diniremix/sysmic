#! /usr/bin/env python
# -*- coding: UTF-8 -*-
try:
	# Intenta usar la versión 2
	import pygtk
	pygtk.require('2.0')
	import gtk
	#usadas al momento de generar un binario
	import cairo, pango, gio, atk, pangocairo
except:
	print "Se necesita install pyGTK o GTKv2, o fijar la variable PYTHONPATH correctamente."
	import sys
	sys.exit(1)

import socket,os,sys

if sys.platform.startswith('linux'):
	os.system('clear')
elif sys.platform.startswith('win'): 
	os.system('cls')

import threading

class FormPreview():
	def __init__(self):
		b= gtk.Builder()
		b.add_from_file("formppal.glade")
		self.frmppal = b.get_object("mainform")
		
		self.mnu = b.get_object("mnubar")
		self.textview = b.get_object("textviewprop")		
		self.statusbar = b.get_object("statusbar")		
		b.connect_signals(self)	
		#buffer para manejar el textview
		self.text_buffer = gtk.TextBuffer()
		#manejar mensajes en la statusbar
		self.context_id = self.statusbar.get_context_id(self.frmppal.get_name())
		self.statusbar.push(self.context_id,self.frmppal.get_title())
		#variables para la conexion del cliente
		self.hostname="localhost"
		self.port=6969
		self.app_version="0.1"
		self.usuario="diniremix"

	#menus de GTK
	def on_mnuconnect_activate(self, widget, data=None):
		#llamada al recibir los datos del server
		self.connect()
		
	def on_mnusaveas_activate(self, widget, data=None):
		print "Guardar como"

	def on_mnuquit_activate(self, widget, data=None):
		print "Salir"
		self.on_window1_destroy(self)		

	#menu ayuda actions
	def on_mnuabout_activate(self, widget, data=None):
		print "Acerca de"		
		self.setbuffer("Hola textviewprop desde python y pyGTK")

	def on_window1_destroy(self, widget, data=None):
		print "saliendo del form..."
		gtk.main_quit()
	
	def setlog(self):
		#f=open("log.dat","a")
		#f.write(msgbuffer)
		#f.close()
		self.bufferlines(msgbuffer)

	def setbuffer(self,msgbuffer):
		self.bufferlines(msgbuffer)
		#self.text_buffer.set_text(msgbuffer)
		#self.textview.set_buffer(self.text_buffer)
	
	def bufferlines(self,msgbuffer):
		enditer = self.text_buffer.get_end_iter()
		self.text_buffer.insert_interactive(enditer, msgbuffer+"\n", True)
		self.textview.set_buffer(self.text_buffer)
	
	#funcion pararecibir el dato del servidor
	def getDato(self,sock):
		return sock.recv(1024)
	
	#funcion main loop
	def mainloop(self,s):
	#Main loop
		i=0
		while True:  
			recibido = self.getDato(s)		
			#No se esta recibiendo datos...		
			if not recibido:
				i=i+1
				if i>10:
					break
			elif recibido=="Temperatura":
				self.setbuffer("Recibiendo Temperatura...")
				recibido = self.getDato(s)		
				if int(recibido)>2500:
					self.setbuffer("Registro de Temperatura Elevada:"+str(recibido)+" grados")
			elif recibido=="Gases":
				self.setbuffer("Recibiendo Gases...")
				recibido = self.getDato(s)		
				if int(recibido)>1500:
					self.setbuffer("Registro de Gases Elevado:"+str(recibido)+" Mt3")
			elif recibido=="Lava":
				self.setbuffer("Recibiendo Lava...")
				recibido = self.getDato(s)		
				if int(recibido)>500:
					self.setbuffer("Registro de Lava Elevado:"+str(recibido)+" Mt2")
			elif recibido=="Humedad":
				self.setbuffer("Recibiendo Humedad...")
				recibido = self.getDato(s)		
				if int(recibido)>700:
					self.setbuffer("Registro de Humedad Elevada:"+str(recibido)+" Hg3")
			elif recibido=="Particulas":
				self.setbuffer("Recibiendo Particulas...")
				recibido = self.getDato(s)		
				if int(recibido)>2000:
					self.setbuffer("Registro de Particulas Elevada:"+str(recibido)+" Mt2")
			elif recibido=="Presion":
				self.setbuffer("Recibiendo Presion...")
				recibido = self.getDato(s)		
				if int(recibido)>1700:
					self.setbuffer("Registro de Presion Elevado:"+str(recibido)+" Mt3")
			if not recibido=="":
				self.setbuffer(recibido)
	#final main loop

	def connect(self):
		try:
			s = socket.socket()  
			print ""
			print "Conectandose a: "+self.hostname+":"+str(self.port)+"..."
			s.connect((self.hostname,self.port))  
			s.send(self.usuario)
			
			recibido=self.getDato(s)
			if recibido=="Getversion":
				s.send(self.app_version)
			
			serverName=self.getDato(s)
			if serverName=="update":
				print "Esta version del cliente necesita una actualizacion."
				sys.exit(1)
			else:
				print "Conexion establecida con el servidor",serverName
				print "Obteniendo estadisticas de",serverName
				print ""	
			
			t=threading.Thread(target=self.mainloop,args=(s,))
			t.start()

		except socket.error, msg:
			print "Ocurrio un error al conectarse al servidor..."
			s.close()
			print "conexion cliente cerrada."
	#connect

if __name__ == "__main__":
	app=FormPreview()
	app.frmppal.show()
	gtk.main()
