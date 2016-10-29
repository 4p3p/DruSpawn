# DruSpawn!
Drupal (Spawn) Scanner!!!!!

Scanner de vulnerabilidades para el CMS favorito del mundo, desarrollado por FCG como parte del proyecto final de PBSCG10.

###Para instalar(En distribuciones de GNU/Linux):
```
git clone https://github.com/f99942/DropAll-Scan
cd  DropAll-Scan
sudo ./install
```

###Método de empleo:
```
sudo druspawn -d drupal.to.check --verbose
```
#####Ejemplo de salida:
```
[**] Modo verboso habilitado 
[**] Inicializando escaneo a http://drupal-7.51/
[**] Se encontro el archivo drupal.js en http://drupal-7.51/misc/drupal.js

[*] "http://drupal-7.51/" se trata de un Drupal 7 
  [*] Version expecifica: 7.51
[**] Este drupal se encuentra actualizado

[*] Tema instalado:
	 bartik

[**] Modulos encontrados en pagina principal: 
[*] => comment
[*] => node
	Posible vulnerabilidad:
	DRUPAL-SA-CONTRIB-2016-007
[*] => search
[*] => system
[*] => content
[*] => field
[*] => user

[***]  Directorios y archivos:
[*] => Respuesta(403) para http://drupal-7.51/includes/ 
[*] => Respuesta(403) para http://drupal-7.51/misc/ 
[*] => Respuesta(403) para http://drupal-7.51/modules/ 
[*] => Respuesta(403) para http://drupal-7.51/profiles/ 
[*] => Respuesta(403) para http://drupal-7.51/scripts/ 
[*] => Respuesta(403) para http://drupal-7.51/sites/ 
[*] => Respuesta(403) para http://drupal-7.51/includes/ 
[*] => Respuesta(403) para http://drupal-7.51/themes/ 
[*] => Respuesta(200) para http://drupal-7.51/robots.txt 
[*] => Respuesta(200) para http://drupal-7.51/xmlrpc.php 
[*] => Respuesta(200) para http://drupal-7.51/CHANGELOG.txt 
[*] => Respuesta(404) para http://drupal-7.51/core/CHANGELOG.txt 

[**] Pagina para ingreso de usuarios:
	 http://192.168.1.148/drupal-7.51//user/login

[***] Ejecucion finalizada 15.5314130783 segundos transcurridos...
```
###Otras opciones que soporta:
```
-h, --help           Muestra la ayuda
-d [http(s)://direccion del escaneo]
                      URL o IP de objetivo a escanear. Este parametro
                      siempre es requerido.
--full                Lista modulos vulnerables instalados en el objetivo,
                      esto basado en vulnerabilidades conocidas, tarda mas
                      tiempo.
-p [http://direccion del proxy]
                      Emplea un proxy(http)
--pdf                 Genera un reporte en formato PDF a partir de el HTML
                      generado
-u [Archivo con user agent]
                      Se especifica un user-agent a traves de un archivo
-s [script.py]        Utiliza un script tuyo, sigue el modelo!!!
--script              Ejecuta solamente el script, ignora los escaneos.
--tor                 Emplea tor como proxy.
--verbose, -v         Habilita el modo verboso, muestra en pantalla los
                      hallazgos.
```

Revise la documentación para información mas detallada en docs/ al clonar el repositorio.

HAVE FUN! ;)
