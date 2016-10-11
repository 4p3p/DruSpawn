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
import argparse
import colors
import os
import time
import getpass

if __name__=="__main__":
    tiempo = time.time()
    log = open(os.getcwd()+'/config/.dropall_scan.log','a')
    parser = argparse.ArgumentParser(description='Scanner de vulnerabilidades \
    para DRUPAL :D')

    parser.add_argument('-d', required=True, nargs=1, help="Direccion de objetivo")
    parser.add_argument('--full', action="store_true", help="Lista versiones de modulos, directorios expuestos y configuraciones de Drupal basado en diccionarios, tarda mas tiempo.")
    parser.add_argument('--listar', action="store_true", help="Lista directorios expuestos y configuraciones de Drupal.")
    parser.add_argument('-m', required=True, nargs=1, help="Pasa como argumento un modulo propio, que aprovecha la conexion de la herramienta")
    parser.add_argument('-p', nargs=1,help="Emplea un proxy, con el fin de mantener el anonimato")
    parser.add_argument('-u', nargs=1, help="Se especifica un user-agent a traves de un archivo")
    parser.add_argument('--ssl',action="store_true",help="conexion cifrada")
    parser.add_argument('--tor',action="store_true",help="Emplea tor como proxy, con el fin de mantener el anonimato")
    parser.add_argument('--verbose','-v',action="store_true",help="Habilita el modo verboso")

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

    if arguments.d:
      print colors.blue('[**] ')+"Inicializando escaneo a %s"%arguments.d[0]
      if 'http' not in arguments.d[0] and not arguments.ssl:
        arguments.d[0]='http://'+arguments.d[0]
      if 'https' not in arguments.d[0] and arguments.ssl:
        arguments.d[0]='https://'+arguments.d[0]
      version.version(req,arguments.d[0],arguments.verbose)
      listar.tema(req,arguments.d[0],arguments.verbose)
      listar.mod_pagina(req,arguments.d[0],arguments.verbose)
      listar.directorios(req,arguments.d[0],arguments.verbose)


    print colors.green('\b\n[***] ')+"Ejecucion finalizada "+format(time.time() - tiempo)+" segundos transcurridos..."