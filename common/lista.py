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
	html = req.get(target).text
	regex = '"theme":"(\w+)"'
	pattern =  re.compile(regex)
	theme = re.findall(pattern,html)
	if theme:
		print colors.green('[*] ')+"Tema instalado: %s\n"%theme[0] if verbose else '',
	else:
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