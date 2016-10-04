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

def version(req, target, verbose=False):
	try:
		js = ['/misc/drupal.js','/core/misc/drupal.js']
		if req.get(target+js[0]).status_code is 200 or req.get(target+js[1]).status_code is 200:
			print colors.green('[**] ')+"Se encontro el archivo drupal.js en %s\n"%(target+js[0]) if req.get(target+js[0]).status_code is 200 and verbose else '',
			print colors.green('\b[**] ')+"Se encontro el archivo drupal.js en %s\n"%(target+js[1]) if req.get(target+js[1]).status_code is 200 and verbose else '',
			html = req.get(target)
			head = html.headers
			if "Drupal 7" in html.text or "Drupal 7" in format(head.values()):
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 7 \n" %target if verbose else '',
				version_exacta67(req, target, 7, verbose)
			elif "Drupal 8" in html.text or "Drupal 8" in format(head.values()):
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 8 \n" %target if verbose else '',
				version_exacta8(req, target, 8, verbose)
			else:
				versiones_posibles(req,target,verbose)
		else:
			print colors.red('\b[*] ')+"Al parecer no se trata de Drupal"
	except:
		print colors.red('\b[***] ')+"Al parecer existen problemas para conectarse al objetivo, verifique que se encuentre funcionando"

def version_exacta67(req, target, version, verbose):
	try:
		objetivo = target+"/modules/system/system.info"
		texto = req.get(objetivo).text
		regex = 'version = "(\d+\.\d+)"'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
			return
		objetivo = target+"/CHANGELOG.txt"
		texto = req.get(objetivo).text
		regex = 'Drupal (\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
			return True
		if version == 7:
			versiones_posibles(req,target,verbose)
		elif version == 6:
			return False
	except:
		print colors.red('[*] ')+"No se pudo obtener la version especifica"	


def version_exacta8(req, target, version, verbose):
	try:
		objetivo = target+"/core/CHANGELOG.txt"
		texto = req.get(objetivo).text
		regex = 'Drupal (\d+\.\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
			return True
		versiones_posibles(req)
	except:
			print colors.red('[*] ')+"No se pudo obtener la version especifica"

def versiones_posibles(req, target, verbose):
	try:
		posibles = []
		actual = os.getcwd()
		versiones = untangle.parse(actual+'/config/versions.xml')
		js = ['/misc/drupal.js','/core/misc/drupal.js']
		if req.get(target+js[0]).status_code is 200:
			hash = hashlib.md5(req.get(target+js[0]).text).hexdigest()
			for v in range(1,len(versiones.root.child[0].version)):
				if versiones.root.child[0].version[v]['md5'] == hash:
					posibles.append(versiones.root.child[0].version[v]['nb'])
			if '6.' in ''.join(posibles):
				print colors.green('\b[*] ')+"\"%s\" se trata de un Drupal 6 \n" %target if verbose else '',
				v = version_exacta67(req,target,6, verbose)
				if v is False:
					print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
					for i in range(1,len(posibles)):
						print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',
				return
			print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
			for i in range(1,len(posibles)):
				print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',
		elif req.get(target+js[1]).status_code is 200:
			hash = hashlib.md5(req.get(target+js[1]).text).hexdigest()
			for v in range(1,len(versiones.root.child[1].version)):
				if versiones.root.child[1].version[v]['md5'] == hash:
					posibles.append(versiones.root.child[1].version[v]['nb'])
			print colors.blue('[***] ')+"Versiones posibles: \n" if verbose else '',
			for i in range(1,len(posibles)):
				print colors.blue('[*] ')+"=> %s \n"%posibles[i] if verbose else '',		
	except:
		print colors.red('[*] ')+"No se pudo obtener la version especifica"