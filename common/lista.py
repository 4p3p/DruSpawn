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

def tema(req, target, verbose=False):
	try:
		html = req.get(target).text
		regex = '"theme":"(\w+)"'
		pattern =  re.compile(regex)
		theme = re.findall(pattern,html)
		if theme:
			pwd = os.getcwd()
			c = sqlite3.connect('/home/fernando/Documents/DrupalScan/config/generadores/drupal_vuln.db')
			con = c.cursor()
			respuesta = con.execute('Select id_vuln,id_proyecto from vulnerabilidades').fetchall()
			print colors.green('[*] ')+"Tema instalado:\n\t %s\n\n"%theme[0] if verbose else '',
			if respuesta:
				for a in respuesta:
					if theme in a[1].replace(' ','_').lower():
						print "\tPosible vulnerabilidad:\n\t%s\n"%a[0] if verbose else '',
		else:
			print colors.red('\n[*] ')+"No se pudo encontrar el tema especifico.\n" if verbose else '',
	except Exception as e:
		print e
		

def mod_pagina(req, target, verbose=False):
	pwd = os.getcwd()
	c = sqlite3.connect('/home/fernando/Documents/DrupalScan/config/generadores/drupal_vuln.db')
	con = c.cursor()
	html = req.get(target).text
	lines = html.split('\n')
	lista_mod=[]
	for line in lines:
			line=line.split("modules")
			if len(line)>1 :
				if line[0][-1] == '/' or line[0][-1:] == '\\\\':
					lista_mod.append(line[1].split("/")[1].split("\\")[0])

	if lista_mod:
		print colors.green('[**] ')+"Modulos encontrados en pagina principal: \n" if verbose else '',
		respuesta = con.execute('Select id_vuln,id_proyecto from vulnerabilidades').fetchall()
		for modulo in list(set(lista_mod)):
			print colors.blue('[*] ')+"=> "+modulo+'\n' if verbose else '',
			for a in respuesta:
				if modulo == a[1].replace(' ','_').lower():
					print "\tPosible vulnerabilidad:\n\t%s\n"%a[0] if verbose else '',

	

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
			i+=1
			print colors.blue('[*] ')+"=> Respuesta("+str(req.get(target+d).status_code)+") para %s \n"%(target+d) if verbose else '',
		except Exception as e:
			print e
			print colors.red('[*] ')+"=> Hubo un problema al intentar acceder a %s, posible redireccionamiento \n"%(target+d) if verbose else '',
			#print colors.red('[*] ')+"Algo salio mal, contacte al equipo de desarrollo"

	if i == 0:
		print colors.green('\t[*] ')+'Wow! no tiene directorios comunes de drupal expuestos o incluso indicios de su existencia!'

	if req.get(target+'/user/login').status_code == 200 and 'password' in req.get(target+'/user/login').text:
		print colors.green('\n[**] ')+"Pagina para ingreso de usuarios:\n\t %s/user/login\n"%target if verbose else '',
	elif req.get(target+'/?q=user/login').status_code == 200 and 'password' in req.get(target+'/?q=user/login').text:
		print colors.green('\n[**] ')+"Pagina para ingreso de usuarios:\n\t %s/?q=user/login\n"%target if verbose else '',
	

def full_scan(req, target, verbose=False):
	try:
		pwd = os.getcwd()
		c = sqlite3.connect('/home/fernando/Documents/DrupalScan/config/generadores/drupal_vuln.db')
		con = c.cursor()
		print colors.green('[***] ')+"Full Scan habilitado, esto puede demorar varios minutos..."
		murls = ['%s/sites/all/modules/%s/','%s/sites/all/modules/%s/README.txt','%s/sites/all/modules/%s/LICENSE.txt','%s/modules/%s/','%s/modules/%s/README.txt','%s/modules/%s/LICENSE.txt']
		turls = ['%s/sites/all/themes/%s/','%s/sites/all/themes/%s/README.txt','%s/sites/all/themes/%s/LICENSE.txt','%s/themes/%s/','%s/themes/%s/README.txt','%s/themes/%s/LICENSE.txt']
		modulos = [line.rstrip() for line in file(os.getcwd()+"/config/modulos.dat").readlines()]
		temas = [line.rstrip() for line in file(os.getcwd()+"/config/temas.dat").readlines()]
		encontrado = []
		tmp = con.execute("Select id_proyecto,id_vuln from vulnerabilidades").fetchall()
		for tema in tmp:
			#print tema[0].replace(' ','_').lower()
			for url in turls:
				if req.get(url%(target,tema[0].replace(' ','_').lower())).status_code in [200,403] and tema[0].replace(' ','_').lower() not in ['',' ','   ']:
					if tema[0].replace(' ','_').lower() not in encontrado:
						encontrado.append(tema[0].replace(' ','_').lower())
						encontrado.append(req.get(url%(target,tema[0].replace(' ','_').lower())).status_code)
					encontrado.append(url%(target,tema[0].replace(' ','_').lower()))
		if encontrado:
			print colors.green('\n[**] ')+"TEMAS O MODULOS ENCONTRADOS CON VULNERABILIDADES: "
			for m in encontrado:
				if 'http' in str(m):
					print '\t\t %s'%m
				else:
					print colors.blue('[**] ')+' %s'%m
					if m not in [200,403]:
						cve = con.execute("select cve.id_cve from cve,vulnerabilidades where vulnerabilidades.id_proyecto like '%s'"%m).fetchone()
						print '\t '+cve[0]
			con.close()
					#tmp = con.execute("Select * from vulnerabilidades where id_proyecto like '\%"+str(m)+"\%'").fetchone()
					#print tmp
					#if tmp:
					#	print "\tPosible vulnerabilidad:"+tmp["id_vuln"]
		else:
			print colors.green('\n\t')+"No se encontraron temas... "
		encontrado = []
		#for modulo in modulos:
		#	for url in murls:
		#		if req.get(url%(target,tema)).status_code in [200,403]:
		#			if tema not in encontrado:
		#				encontrado.append(tema)
		#				encontrado.append(req.get(url%(target,tema)).status_code)
		#			encontrado.append(url%(target,tema))
		#if encontrado:
		#	print colors.green('\n[**] ')+"MODULOS ENCONTRADOS: "
		#	for m in encontrado:
		#		if 'http' in str(m):
		#			print '\t\t %s'%m
		#		else:
		#			print '\t %s'%m
					#tmp = con.execute("Select * from vulnerabilidades where id_proyecto like '\%"+str(m)+"\%'").fetchone()
					#print tmp
					#if tmp:
					#	print "\tPosible vulnerabilidad:"+tmp["id_vuln"]
		#else:
		#	print colors.green('\n\t')+"No se encontraron temas... "
		#print encontrado
	except Exception as e:
		print e