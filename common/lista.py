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

def tema(req, target, verbose=True):
	html = req.get(target).text
	regex = '"theme":"(\w+)"'
	pattern =  re.compile(regex)
	theme = re.findall(pattern,html)
	if theme:
		print colors.green('[*] ')+"Tema instalado: %s"%theme[0] if verbose else '',
	else:
		print colors.red('[*] ')+"No se pudo encontrar el tema especifico." if verbose else '',