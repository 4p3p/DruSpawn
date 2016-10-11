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
import sqlite3
import untangle
import re

def contrib(con):
  contrib = ["https://www.drupal.org/project/project_theme?page=%d","https://www.drupal.org/project/project_module?page=%d"]
  for burl in contrib:
    i=0
    while True:
      count = 0
      url = burl %(i)
      r = requests.get(url)
      if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        for link in soup.findAll('a'):
          if link.parent.name == 'h2':
            if link.has_key('href') and not link.has_key('rel'):
              uri = link['href']
              link = link["href"].split("/")
              if link[1] == "project":
                count = count + 1
                if burl == contrib[0]:
                  con.execute('insert or ignore into contributed values(?,?,?)',(link[2],"theme","https://www.drupal.org"+uri))
                  print "Insertando %s %s %s"%(link[2],"theme","https://www.drupal.org"+uri)
                elif burl == contrib[1]:
                  con.execute('insert or ignore into contributed values(?,?,?)',(link[2],"module","https://www.drupal.org"+uri))
                  print "Insertando %s %s %s"%(link[2],"module","https://www.drupal.org"+uri)
        if count == 0:
          break
      if count != 25:
        print "Count not 25 at %d" %(i)
      i = i + 1

def core(con):
  actual = os.getcwd()
  versiones = untangle.parse(actual+'/../versions.xml')
  for i in range(0,2):
    for v in range(1,len(versiones.root.child[i].version)):
      con.execute('insert into core values(?,?)',(versiones.root.child[i].version[v]['nb'],versiones.root.child[i].version[v]['md5']))
      print "Insertando %s, %s"%(versiones.root.child[i].version[v]['nb'],versiones.root.child[i].version[v]['md5'])

def vulns(con):
  dirs = ['https://www.drupal.org/security?page=%d','https://www.drupal.org/security/contrib?page=%d']
  #https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5385
  for burl in dirs:
    i=0
    txt = requests.get(burl %(i))
    if txt.status_code == 200:
      sopa = BeautifulSoup(txt.text)
      li = sopa.findAll("li", { "class" : "pager-last last" })
    regex = '.*page=(\d+)'
    pattern =  re.compile(regex)
    n = re.findall(pattern,format(li[0]))
    for i in range (0,int(n[0])+1):
      url = burl %(i)
      r = requests.get(url)
      if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        for link in soup.findAll('a'):
          if link.parent.name == 'h2':
            if link.has_key('href') and not link.has_key('rel'):
              uri = link['href']
              vuln = requests.get('https://www.drupal.org'+uri).text
              pattern =  re.compile('.*ID: (\w+-\w+-\w+-\w+-\w+)')
              id_vuln = re.findall(pattern,vuln)
              if id_vuln:
                print id_vuln[0]
                pattern =  re.compile('.*Project: <.*>(\w+ *\w*).*<.*')
                proyecto = re.findall(pattern,vuln)
                if proyecto:
                  print proyecto[0].replace(' ','_').lower()
                else:
                  proyecto=['']
                pattern =  re.compile('.*Version: *(.*).*<')
                version = re.findall(pattern,vuln)
                if version:
                  print version[0]
                else:
                  version = ['']
                pattern =  re.compile('.*Date: *(.*).*<')
                fecha = re.findall(pattern,vuln)
                if fecha:
                  print fecha[0]
                else:
                  fecha = ['']
                pattern =  re.compile('.*Security risk: *(\w+/\w+|\w+ *\w*)')
                riesgo = re.findall(pattern,vuln)
                if riesgo:
                  print riesgo[0]
                else:
                  riesgo = ['']
                #tipo IMPLEMENTALO!!!
                #Descripcion
                descripcion = ['']
                #solucion
                solucion = ['']
                #cve
                pattern =  re.compile('.*(CVE-\d+-\d+)')
                cve = re.findall(pattern,vuln)
                if cve:
                  for e in cve:
                    con.execute('insert or ignore into cve values(?,?,?)',(e,id_vuln[0],"https://cve.mitre.org/cgi-bin/cvename.cgi?name="+e))
                    print "Insertando %s %s %s en cve"%(e,id_vuln[0],"https://cve.mitre.org/cgi-bin/cvename.cgi?name="+e)
                con.execute('insert or ignore into vulns values(?,?,?,?,?,?,?,?)',(id_vuln[0],proyecto[0],version[0],fecha[0],riesgo[0],descripcion[0],solucion[0],'https://www.drupal.org'+uri))
                print "Insertando %s\n%s\n%s\n%s\n%s\n%s\n%s\n%s"%(id_vuln[0],proyecto[0],version[0],fecha[0],riesgo[0],descripcion[0],solucion[0],'https://www.drupal.org'+uri)

if __name__=="__main__": 
  pwd = os.getcwd()
  c = sqlite3.connect(pwd+'/drupal_vuln.db')
  con = c.cursor()
  #contrib(c)
  #core(c)
  vulns(c)
  c.commit()
  c.close()