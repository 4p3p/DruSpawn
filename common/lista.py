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

	mod = ["%ssites/all/modules/%s/","%ssites/default/modules/%s/", "%s/modules/%s/"]
	for modulo in list(set(lista_mod)):


	

def directorios(req, target, verbose=False):
	dirs = ['/includes/',
	'/misc/',
	'/modules/',
	'/profiles/',
	'/scripts/',
	'/sites/',
	'/includes/',
	'/themes/',
	'/core/',
	'user/login']
	for d in dirs:
		try:
			if req.get(target+d).status_code == 403:
				print "%s esta prohibido"%(target+d)
			elif req.get(target+d).status_code == 300:
				print "%s tiene redireccion"%(target+d)
			elif req.get(target+d).status_code == 200:
				print "%s esta abierto"%(target+d)
			else:
				print req.get(target+d).status_code
		except:
			print "No sirve"

#def modulos(req, target, verbose=False):