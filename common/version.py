#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import urllib2
import re
import colors

def version(target, proxy=False, verbose=False, user_agent=''):
	try:
		req = urllib2.Request(target)
		if user_agent is not '':
			req.add_header('User-agent',user_agent[:-1])
		html = urllib2.urlopen(req).read()
		head = urllib2.urlopen(req).info()
		if "Drupal 6" in html or "Drupal 6" in head:
			print colors.green('[*] ')+"Al parecer \"%s\" se trata de un Drupal 6" %target
			version_exacta67(target)
		if "Drupal 7" in html or "Drupal 7" in head:
			print colors.green('[*] ')+"Al parecer \"%s\" se trata de un Drupal 7" %target
			version_exacta67(target,7)
		elif "Drupal 8" in html or "Drupal 7" in head:
			print colors.green('[*] ')+"Al parecer \"%s\" se trata de un Drupal 8" %target
			version_exacta8(target,8)
		else:
			print colors.red('[*] ')+"Al parecer no se trata de Drupal"
	except:
		print colors.red('[***] ')+"Al parecer existen problemas para conectarse al objetivo, verifique que se encuentre funcionando"

def version_exacta67(target, version):
	try:
		objetivo = target+"/modules/system/system.info"
		texto = urllib2.urlopen(objetivo).read()
		regex = 'version = "(\d+\.\d+)"'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
			return
		objetivo = target+"/CHANGELOG.txt"
		texto = urllib2.urlopen(objetivo).read()
		regex = 'Drupal (\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
			return
		print colors.red('[*] ')+"No se pudo obtener la version especifica"
	except:
		print colors.red('[*] ')+"No se pudo obtener la version especifica"	


def version_exacta8(target, version):
	try:
		objetivo = target+"/core/CHANGELOG.txt"
		texto = urllib2.urlopen(objetivo).read()
		regex = 'Drupal (\d+\.\d+\.\d+),'
		pattern =  re.compile(regex)
		version_x = re.findall(pattern,texto)
		if version_x:
			print colors.green('[*] ')+"Version expecifica: %s"%version_x[0]
	except:
			print colors.red('[*] ')+"No se pudo obtener la version especifica"