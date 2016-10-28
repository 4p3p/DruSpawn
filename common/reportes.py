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
import getpass

def create(target,tiempo,usuario,args,ip,user_agent):
	i=1
	pwd = os.getcwd()
	if 'https' in target:
		titulo = str(target.replace('https://','').replace('/','')+datetime.datetime.now().strftime("%a%d%s"))
	else:
		titulo = str(target.replace('http://','').replace('/','')+datetime.datetime.now().strftime("%a%d%s"))
	if 'root' in getpass.getuser():
		ubicacion = '/'+getpass.getuser()+'/.drustroyer/reportes/'+ titulo
	else
		ubicacion = '/home/'+getpass.getuser()+'/.drustroyer/reportes/'+ titulo
	if not os.path.exists(ubicacion):
		os.makedirs(ubicacion)
	if 'root' in getpass.getuser():
		os.system('sudo cp -rf /opt/drustroyer/reportes/dependencias/ /'+getpass.getuser()+'/.drustroyer/reportes/'+titulo+'/')
	else
		os.system('sudo cp -rf /opt/drustroyer/reportes/dependencias/ /home/'+getpass.getuser()+'/.drustroyer/reportes/'+titulo+'/')	
	reporte = open(ubicacion+'/'+titulo,'a')
	reporte.write('''
<html>
<head>
	<title>Reporte</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
	<link rel="stylesheet" href="dependencias/style.css" type="text/css" />
</head>
<body>
	<div id="wrap">
		<div id="header">
			<h1 id="logo-text">DrupalScan</h1>
			<h2 id="slogan">Reporte de escaneo a %s</h2>
			<div id="header-links">
				<p> <a href="https://www.drupal.org">DRUPAL</a> | <a href="https://seguridad.unam.mx">UNAM CERT</a> | <a href="#">FCG</a> </p>
			</div>
		</div>
		<div id="content-wrap">
			<div id="sidebar">
				<h1>ARGUMENTOS</h1>
				<ul class="sidemenu">
		'''%target)


	for key,value in args.iteritems():
		reporte.write('''
					<li><strong>-%s: </strong>%s</li>'''%(key,value))
	reporte.write('''
				</ul>
			</div>''')

	reporte.write('''	
			<div id="main">
				<h1>INFORMACION GENERAL</h1>
				<strong>OBJETIVO: </strong><a href="%s">%s</a><br/>
				<strong>INICIO DE ESCANEO: </strong>%s<br/>
				<strong>USUARIO: </strong>%s<br/>
				<strong>IP: </strong>%s<br/>
				<strong>USER-AGENT: </strong>%s<br/>
			</div>
		'''%(target,target,tiempo,usuario,ip,user_agent))
	return reporte

def version(reporte, lista):
	reporte.write('''
			<div id="main">
				<h1>INFORMACION DE LA VERSION</h1>
			''')
	for elemento in lista:
		reporte.write('''
				%s
				'''%elemento)
	reporte.write('''
			</div>
				''')

def listado(reporte,lista):
	reporte.write('''
			<div id="main">
				<h1>DIRECTORIOS, TEMAS Y MODULOS.</h1>
			''')
	for elemento in lista:
		reporte.write('''
				%s
				'''%elemento)

	reporte.write('''
			</div>
				''')

def vuln(reporte,listalista):
	reporte.write('''
				<div id="main">
					<h1>VULNERABILIDADES POSIBLES PARA SECCION.</h1>
					<table>
					<tr>
						<th class="first"><strong>ID</strong> vulnerabilidad</th>
						<th>Informacion</th>
						<th>CVEs</th>
					</tr>
				''')
	cves = ''
	for i in range(0,len(listalista)-1):
		if listalista[i][1]:
			for j in range(0,len(listalista[i])-1):
				for k in range(0,len(listalista[j])-1):
					cves += '<strong><a href="'+str(listalista[i][1][k][1])+'">'+str(listalista[i][1][k][0])+"</a></strong><br/> "
	flag = True
	for i in range(0,len(listalista)):
		for j in range(0,len(listalista[i])-1):
			for k in range(0,len(listalista[j])-1):
				if flag:
					reporte.write('''
					<tr class="row-a">
					''')
					flag = False
				else:
					reporte.write('''
					<tr class="row-b">
					''')
					flag = True
				reporte.write('''
						<td class="first"><a href='%s'>%s</a></td>
						<td>
						<strong>PROYECTO:</strong></br><p>%s</p>
						<strong>FECHA:</strong></br><p>%s</p>
						<strong>NIVEL:</strong></br><p>%s</p>
						<strong>TIPO:</strong></br><p>%s</p>
						</td>
						<td>%s</td>
					</tr>
					'''%(listalista[i][0][j][5],listalista[i][0][j][0],listalista[i][0][j][1],listalista[i][0][j][2],listalista[i][0][j][3],listalista[i][0][j][4],cves))
	reporte.write('''
					</tr>
		      </table>
		    </div>
		''')

def full(reporte,lista):
	reporte.write('''
			<div id="main">
				<h1>FULL SCAN.</h1>
			''')
	for elemento in lista:
		reporte.write('''
				%s
				'''%elemento)

	reporte.write('''
			</div>
				''')

def script(nombre,cadena,reporte):
	reporte.write('''
			<div id="main">
				<h1>SCRIPT: %s</h1>
				<strong>VALOR DE RETORNO: </strong><br/>
				<p>%s</p>
			</div>'''%(nombre,cadena))

def finalizar(reporte):
	reporte.write('''
		<br />
		</div>
		<div id="footer">
			<p> &copy; 2016 <strong>UNAM CERT</strong></p>
		</div>
	</div>	
</body>
</html>
		''')