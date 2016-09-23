#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
       ___                         __ ____
      / _ \ ____ __ __ ___  ___ _ / // __/____ ___ _ ___
     / // // __// // // _ \/ _ `// /_\ \ / __// _ `// _ \
    /____//_/   \_,_// .__/\_,_//_//___/ \__/ \_,_//_//_/
                    /_/
'''
__author__="Fernando Castaneda G."
__copyright__="Copyright 2016, UNAM-CERT"
__license__="GPL"
__version__="0.1"
__status__="Prototype"

import common.version as version
import common.lista as listar
import argparse
import colors

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Scanner de vulnerabilidades \
    para DRUPAL :D')
    parser.add_argument('-d', required=True, nargs=1, help="Direccion de objetivo")
    parser.add_argument('--listar', action="store_true", help="Lista directorios expuestos y configuraciones de Drupal.")
    parser.add_argument('-u', nargs=1, help="Se especifica un user-agent a traves de un archivo")
    parser.add_argument('--proxy',action="store_true",help="Emplea tor como proxy, con el fin de mantener el anonimato")
    parser.add_argument('--verbose','-v',action="store_true",help="Habilita el modo verboso")
    verbose=False
    useragent=''

    arguments = parser.parse_args()

    if arguments.verbose:
      verbose=True
      print colors.yellow('[**] ')+"Modo verboso habilitado"

    if arguments.u:
      f=open(arguments.u[0])
      useragent=f.read()
      print colors.yellow('[**] ')+"Empleando \"%s\" como User-agent"%useragent[:-1]

    if arguments.d:
      print colors.blue('[**] ')+"Inicializando escaneo a %s"%arguments.d[0]
      if 'http' not in arguments.d[0]:
        print colors.red('[**] ')+"Formato requerido http://url_de_drupal o http://ip_de_drupal"
      else:
        version.version(arguments.d[0],arguments.proxy,arguments.verbose,useragent)
        if arguments.listar:
          listar.tema(arguments.d[0])
          listar.dir(arguments.d[0])