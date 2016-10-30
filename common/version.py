#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="UNAM CERT"
__version__="1.0"
__status__="Prototype"

import requests
import re
import colors
import requesocks
import untangle
import hashlib
import os
import reportes
import sys
import sqlite3

def version(req, target, verbose, archivo):
	reporte = []
	try:
		js = ['/misc/drupal.js','/core/misc/drupal.js']
		if req.get(target+js[0]).status_code is 200 or req.get(target+js[1]).status_code is 200:
			if req.get(target+js[0]).status_code is 200:
				print colors.green('[**] ')+"Se encontro el archivo drupal.js en %s\n"%(target+js[0]) if req.get(target+js[0]).status_code is 200 and  verbose else '', 
				reporte.append("Se encontro el archivo drupal.js en <a href='%s'>%s</a><br/>"%(target+js[0],target+js[0]))
			if req.get(target+js[1]).status_code is 200:
				print colors.green('\b[**] ')+"Se encontro el archivo drupal.js en %s\n"%(target+js[1]) if req.get(target+js[1]).status_code is 200 and verbose else '',
				reporte.append("Se encontro el archivo drupal.js en <a href='%s'>%s</a><br/>"%(target+js[1],target+js[1]))
			html = req.get(target)
			head = html.headers
			if "Drupal 7" in html.text or "Drupal 7" in format(head.values()):
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 7 \n" %target if verbose else '',
				reporte.append("<strong>\"%s\"</strong> se trata de un Drupal 7<br/>" %target)
				version_exacta67(req, target, 7, verbose,reporte, archivo)
			elif "Drupal 8" in html.text or "Drupal 8" in format(head.values()):
				reporte.append("<strong>\"%s\"</strong> se trata de un Drupal 8<br/>" %target)
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 8 \n" %target if verbose else '',
				version_exacta8(req, target, 8, verbose, reporte, archivo)
			else:
				versiones_posibles(req,target,verbose, reporte, archivo)
		else:
			print colors.red('\b[*] ')+"Al parecer no se trata de Drupal"
			sys.exit()
	except Exception as e:
		#print e
		print colors.red('\b[***] ')+"Al parecer existen problemas para conectarse al objetivo, verifique que se encuentre funcionando"
		#sys.exit()

def version_exacta67(req, target, version, verbose, reporte, archivo):
	try:
		objetivo = target+"/modules/system/system.info"
		texto = req.get(objetivo).text
		regex = 'version = "(\d+\.\d+)"'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s\n"%version_x[0] if verbose else '',
			reporte.append("Version expecifica: %s<br/>"%version_x[0])
			actualizado(req,version_x[0],verbose, reporte, archivo)
			return True
		objetivo = target+"/CHANGELOG.txt"
		texto = req.get(objetivo).text
		regex = 'Drupal (\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s\n"%version_x[0] if verbose else '',
			reporte.append("Version expecifica: %s<br/>"%version_x[0])
			actualizado(req,version_x[0],verbose, reporte, archivo)
			return True
		if version == 7:
			versiones_posibles(req,target,verbose, reporte, archivo)
		elif version == 6:
			return False
	except:
		print colors.red('[*] ')+"No se pudo obtener la version especifica\n"	if verbose else '',
		reporte.append("No se pudo obtener la version especifica<br/>")


def version_exacta8(req, target, version, verbose,reporte,archivo):
	try:
		objetivo = target+"/core/CHANGELOG.txt"
		texto = req.get(objetivo).text
		regex = 'Drupal (\d+\.\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s\n"%version_x[0] if verbose else '',
			reporte.append("Version expecifica: %s<br/>"%version_x[0])
			actualizado(req,version_x[0],verbose)
			return True
		versiones_posibles(req)
	except:
		print colors.red('[*] ')+"No se pudo obtener la version especifica\n" if verbose else '',
		reporte.append("No se pudo obtener la version especifica<br/>")

def versiones_posibles(req, target, verbose, reporte, archivo):
	try:
		posibles = []
		versiones = untangle.parse('/opt/druspawn/config/versions.xml')
		js = ['/misc/drupal.js','/core/misc/drupal.js']
		if req.get(target+js[0]).status_code is 200:
			hash = hashlib.md5(req.get(target+js[0]).text).hexdigest()
			for v in range(1,len(versiones.root.child[0].version)):
				if versiones.root.child[0].version[v]['md5'] == hash:
					posibles.append(versiones.root.child[0].version[v]['nb'])
			if '6.' in ''.join(posibles):
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 6 \n" %target if verbose else '',
				reporte.append("\"%s\" se trata de un Drupal 6<br/>" %target)
				v = version_exacta67(req,target,6, verbose,reporte, archivo)
				if v is False:
					if posibles:
						print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
						reporte.append("Versiones posibles(Obtenidas del hash de drupal.js): <br/>")
						reporte.append("<ul>")
						u = 0
						for i in range(1,len(posibles)):
							print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',
							reporte.append("<li> %s </li>"%posibles[i])
							u = i
						reporte.append('</ul>')
						actualizado(req,posibles[u],verbose, reporte, archivo)
					else:
						print colors.blue('[***] ')+"No se pudo obtener la version especifica \n" if verbose else '',
						reporte.append("No se pudo obtener la version especifica<br/>")
				return
			print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
			reporte.append("Versiones posibles(Obtenidas del hash de drupal.js): ")
			reporte.append("<ul>")
			for i in range(1,len(posibles)):
				print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',
				reporte.append("<li> %s </li>"%posibles[i])
			reporte.append("</ul>")
			actualizado(req,posibles[-1],verbose, reporte, archivo)
		elif req.get(target+js[1]).status_code is 200:
			hash = hashlib.md5(req.get(target+js[1]).text).hexdigest()
			reporte.append("Versiones posibles(Obtenidas del hash de drupal.js): ")
			reporte.append("<ul>")
			for v in range(1,len(versiones.root.child[1].version)):
				if versiones.root.child[1].version[v]['md5'] == hash:
					posibles.append(versiones.root.child[1].version[v]['nb'])
			print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
			for i in range(1,len(posibles)):
				print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',
				reporte.append("<li> %s </li>"%posibles[i])
			reporte.append("</ul>")	
			actualizado(req,posibles[-1],verbose, reporte, archivo)	
	except Exception as e:
		#print e
		print colors.red('[*] ')+"No se pudo obtener la version especifica" if verbose else '',
		reporte.append("</ul>")

def actualizado(req,version,verbose, reporte, archivo):
	try:
		#print version
		if '8' in str(version):
			pattern = re.compile('Drupal core (8\.\d\.\d)')
			ultima = re.findall(pattern,req.get('https://www.drupal.org/project/drupal').text)
		elif '7' in str(version):
			pattern = re.compile('Drupal core (7\.\d+)')
			ultima = re.findall(pattern,req.get('https://www.drupal.org/project/drupal').text)
		elif '6' in str(version):
			reporte.append('La ultima version de Drupal 6 es la 6.38, la cual no es mantenida desde el <strong>24 de febrero de 2016</strong>')
			escribe(archivo,reporte)
			vulnerabilidad(version, archivo,reporte,verbose)
			return
		if str(version) in ultima:
			print colors.green('[**] ')+"Este drupal se encuentra actualizado\n\n" if verbose else '',
			reporte.append("Este drupal se encuentra actualizado, obtenido de <a href='https://www.drupal.org/project/drupal'>https://www.drupal.org/project/drupal</a>")
		else:
			print colors.red('[**] ')+"Este sitio no se encuentra actualizado\n\n" if verbose else '',
			reporte.append("Este drupal no se encuentra actualizado")
			reporte.append("La version mas reciente es: "+ultima[0])
			reporte.append("Consultado de <a href='https://www.drupal.org/project/drupal'>https://www.drupal.org/project/drupal</a>")
		escribe(archivo,reporte)
		vulnerabilidad(version, archivo,reporte, verbose)
	except Exception as e:
		print e
		print colors.red('[++] ')+"No se puede definir si Drupal se encuentra actualizado\n\n" if verbose else '',
		reporte.append("No se puede definir si Drupal se encuentra actualizado")
		escribe(archivo,reporte)
		vulnerabilidad(version, archivo,reporte, verbose)

def vulnerabilidad(version, archivo,reporte, verbose):
	try:
		vulnes = []
		c = sqlite3.connect('/opt/druspawn/config/generadores/drupal_vuln.db')
		con = c.cursor()
		respuesta = con.execute('Select v.id_vuln,v.id_proyecto,v.solucion from vulnerabilidades as v,core as c where v.id_proyecto like "%core"').fetchall()
		vulns = []
		if respuesta:
			for a in respuesta:
				if '6' in version:
					r = re.compile('Drupal core (6\.\d+)')
				elif '7' in version:
					r = re.compile('Drupal core (7\.\d+)')
				elif '8' in version:
					r = re.compile('Drupal core (8\.\d+)')
				versiones = re.findall(r,a[2])
				if versiones:
					for v  in versiones:
						if float(version) < float(v):
							vulns.append(a[0])
		if vulns:
			print "Posibles vulnerabilidades para este CORE:\n " if verbose else '',
			for v in list(set(vulns)):
				print v+'\n' if verbose else '',
				respuesta = con.execute("Select v.id_vuln,v.id_proyecto,v.fecha,v.nivel,v.tipo,v.url from vulnerabilidades as v where v.id_vuln='%s'"%v).fetchall()
				cves = con.execute("Select id_cve,url from cve where id_vuln='%s'"%v).fetchall()
				vulnes.append([respuesta,cves])
			reportes.vuln(archivo,vulnes)
	except Exception as e:
		print e

def escribe(archivo,reporte):
	reportes.version(archivo,reporte)