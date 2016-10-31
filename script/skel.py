#!/usr/bin/python
'''
skel.py

El universo es el limite...

Ten en cuenta que debes tener siempre dos parametros vivos, la conexion y el objetivo.
Los nombres para estos objetos se encuentran asignados por defecto, pueden cambiarse

retorno = 'Esta variable siempre debera ser una cadena de texto, la cual se imprimira en el reporte'
'''

import sys #Para obtener los parametros a traves de linea de comandos
import requests #Para hacer peticiones.
import requesocks #Para hacer peticiones con un proxy.

conexion,target = sys.argv[1],sys.argv[2]
retorno = ''

dependencia = open('/opt/druspawn/script/dependencias/skel.txt','r')

retorno = dependencia.read()