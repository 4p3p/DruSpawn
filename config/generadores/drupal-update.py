#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import requests
import sys
import os
from BeautifulSoup import BeautifulSoup

def diccionarios(tipo):
  if tipo == 1:
    f = open(os.getcwd()+"/../temas.dat",'w')
    burl = "http://www.drupal.org/project/project_theme?page=%d"
    resource = "themes"
  elif tipo == 2:
    f = open(os.getcwd()+"/../modulos.dat",'w')
    burl = "http://www.drupal.org/project/project_module?page=%d"
    resource = "modules"
  i=0
  while True:
    count = 0
    url = burl %(i)
    r = requests.get(url)
    if r.status_code == 200:
      if i%1 == 0:
        print "Escaneando pagina %d de %s"%(i+1, resource)
      soup = BeautifulSoup(r.text)
      for link in soup.findAll('a'):
        if link.parent.name == 'h2':
          if link.has_key('href') and not link.has_key('rel'):
            link = link["href"].split("/")
            if link[1] == "project":
              count = count + 1
              f.write(link[2])
              f.write("\n")
      if count == 0:
        break
    if count != 25:
      print "Count not 25 at %d" %(i)
    i = i + 1


diccionarios(1)
diccionarios(2)