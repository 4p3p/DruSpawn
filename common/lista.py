#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import colors
import urllib2
import re

def tema(target):
	html = urllib2.urlopen(target).read()
	regex = '"theme":"(\w+)"'
	pattern =  re.compile(regex)
	theme = re.findall(pattern,html)
	if theme:
		print colors.green('[*] ')+"Tema instalado: %s"%theme[0]
	else:
		print colors.red('[*] ')+"No se pudo encontrar el tema especifico."

def dir(target):
	dirs = ['/includes/',
	'/misc/',
	'/modules/',
	'/profiles/',
	'/scripts/',
	'/sites/',
	'/includes/',
	'/themes/']
	for d in dirs:
		try:
			if urllib2.urlopen(target+d).getcode() is 200:
				print colors.green('[*] ')+"Respuesta desde: %s"%(target+d)
		except urllib2.URLError as e:
			pass