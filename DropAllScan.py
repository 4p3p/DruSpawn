#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import common.version as version
import common.lista as listar
import common.session as session
import common.reportes as report
import argparse
import colors
import os, sys
import time
import getpass
import subprocess

if __name__=="__main__":
    tiempo = time.time()
    if 'root' in getpass.getuser():
      log = open('/'+getpass.getuser()+'/.drustroyer/logs/exec.log','a')
    else:
      log = open('/home/'+getpass.getuser()+'/.drustroyer/logs/exec.log','a')
    parser = argparse.ArgumentParser(description='Scanner para DRUPAL, funciona con las versiones 6, 7 y 8 del CMS favorito del mundo ;)')
    parser.add_argument('-d', metavar ='[http(s)://direccion del escaneo]', required=True, nargs=1, help="URL o IP de objetivo a escanear. Este parametro siempre es requerido.")
    parser.add_argument('--full', action="store_true", help="Lista modulos vulnerables instalados en el objetivo, esto basado en vulnerabilidades conocidas, tarda mas tiempo.")
    parser.add_argument('-p', metavar='[http://direccion del proxy]', nargs=1,help="Emplea un proxy(http)")
    parser.add_argument('--pdf',action='store_true',help="Genera un reporte en formato PDF a partir de el HTML generado")
    parser.add_argument('-u', metavar='[Archivo con user agent]', nargs=1, help="Se especifica un user-agent a traves de un archivo")
    parser.add_argument('-s', metavar='[script.py]' ,nargs=1,help="Utiliza un script tuyo, sigue el modelo!!!")
    parser.add_argument('--script',action="store_true",help="Ejecuta solamente el script, ignora los escaneos.")
    parser.add_argument('--tor',action="store_true",help="Emplea tor como proxy.")
    parser.add_argument('--verbose','-v',action="store_true",help="Habilita el modo verboso, muestra en pantalla los hallazgos.")

    verbose=False
    useragent=''
    arguments = parser.parse_args()
    proxy = ''

    log.write("Ejecucion en "+time.asctime(time.localtime(time.time()))+"\n Usuario: "+getpass.getuser()+'\n Argumentos: %s\n'%format(vars(arguments))+'-'*200+"\n")

    if arguments.verbose:
      verbose=True
      print colors.yellow('[**] ')+"Modo verboso habilitado"

    if arguments.p:
      proxy = arguments.p[0]
      print colors.yellow('[**] ')+"Empleando \"%s\" como proxy"%proxy

    if arguments.u:
      f=open(arguments.u[0])
      useragent=f.read()
      print colors.yellow('[**] ')+"Empleando \"%s\" como User-agent"%useragent[:-1]

    req = session.session_parameters(arguments.tor,useragent,arguments.verbose, proxy)

    if not arguments.script:
      if arguments.d:
        reporte = report.create(arguments.d[0],time.asctime(time.localtime(time.time())),getpass.getuser(),vars(arguments),req.get('http://ipecho.net/plain').text,useragent[:-1])
        print colors.blue('[**] ')+"Inicializando escaneo a %s"%arguments.d[0]
        if 'http' not in arguments.d[0]:
          arguments.d[0]='http://'+arguments.d[0]
        version.version(req,arguments.d[0],arguments.verbose,reporte)
        listar.general(req,arguments.d[0],arguments.verbose,reporte)
        if arguments.full:
          listar.full_scan(req,arguments.d[0],arguments.verbose,reporte)
        if arguments.s:
          script = "/opt/drustroyer/script/"
          sys.argv = [script+arguments.s[0], req, arguments.d[0]]
          retorno = dict()
          execfile(script+arguments.s[0], dict(), retorno)
          report.script(arguments.s[0],retorno["retorno"],reporte)       
    elif arguments.script and arguments.d:
      if arguments.s:
        reporte = report.create(arguments.d[0],time.asctime(time.localtime(time.time())),getpass.getuser(),vars(arguments),req.get('http://ipecho.net/plain').text,useragent[:-1])
        print colors.green('[**] ')+"Ejecutando unicamente script %s sobre %s"%(arguments.s[0],arguments.d[0])
        script = "/opt/drustroyer/script/"
        sys.argv = [script+arguments.s[0], req, arguments.d[0]]
        retorno = dict()
        execfile(script+arguments.s[0], dict(), retorno)
        report.script(arguments.s[0],retorno["retorno"],reporte)
      elif not arguments.s:
        print colors.red('[**] ')+"Debes seleccionar un script para usar la opcion --script"

    if reporte:
      report.finalizar(reporte)
    #if arguments.pdf:
    #  report.pdf()
    print colors.green('\b\n\n[***] ')+"Ejecucion finalizada "+format(time.time() - tiempo)+" segundos transcurridos..."