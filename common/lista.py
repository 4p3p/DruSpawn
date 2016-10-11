#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import requests
import re
import colors
import requesocks
import untangle
import hashlib
import os

def tema(req, target, verbose=False):
	try:
		html = req.get(target).text
		regex = '"theme":"(\w+)"'
		pattern =  re.compile(regex)
		theme = re.findall(pattern,html)
		if theme:
			print colors.green('[*] ')+"Tema instalado: %s\n"%theme[0] if verbose else '',
		else:
			print colors.red('[*] ')+"No se pudo encontrar el tema especifico." if verbose else '',
	except:
		print colors.red('[*] ')+"No se pudo encontrar el tema especifico." if verbose else '',

def mod_pagina(req, target, verbose=False):
	html = req.get(target).text
	lines = html.split('\n')
	lista_mod=[]
	for line in lines:
			line=line.split("modules")
			if len(line)>1 :
				if line[0][-1] == '/' or line[0][-1:] == '\\\\':
					lista_mod.append(line[1].split("/")[1].split("\\")[0])

	if lista_mod and verbose:
		print colors.green('[**] ')+"Modulos encontrados en pagina principal: "
		for modulo in list(set(lista_mod)):
			print colors.blue('[*] ')+"=> "+modulo

	

def directorios(req, target, verbose=False):
	dirs = ['/includes/',
	'/misc/',
	'/modules/',
	'/profiles/',
	'/scripts/',
	'/sites/',
	'/includes/',
	'/themes/'] 
	i = 0
	print colors.green('\n[***] ')+' Directorios:\n' if verbose else '',
	for d in dirs:
		try:
			if req.get(target+d).status_code == 403:
				i+=1
				print colors.blue('[*] ')+"=> Existe en servidor(no accesible) %s \n"%(target+d) if verbose else '',
			elif req.get(target+d).status_code == 200:
				i+=1
				print colors.yellow('[*] ')+"Existe en servidor(accesible) %s \n"%(target+d) if verbose else '',
		except:
			print colors.red('[*] ')+"Algo salio mal, contacte al equipo de desarrollo"

	if i == 0:
		print colors.green('\t[*] ')+'Wow! no tiene directorios comunes de drupal expuestos o incluso indicios de su existencia!'

	if req.get(target+'/?q=user/login').status_code == 200:
		print colors.green('\n[**] ')+"Pagina para ingreso de usuarios:\n\t %s/?q=user/login"%target if verbose else '',

#def modulos(req, target, verbose=False):
	#TERMINA DE MIGRAR A REQUESTS!!!!!!!!!!!!!!