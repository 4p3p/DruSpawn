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
import sqlite3
import datetime

def create(target):
	i=1
	titulo = str(target.replace('http://','')+datetime.datetime.now().strftime("%a%d"))
	ubicacion = os.getcwd()+"/../reportes/"+ titulo
	if not os.path.exists(ubicacion):
		os.makedirs(ubicacion)
	reporte = open(ubicacion+'/'+titulo,'w')
	reporte.write('<html>\n\t<head>\n\t</head>\n<body>')
	return 


create('google.com')

def append(cadena):


#def final()