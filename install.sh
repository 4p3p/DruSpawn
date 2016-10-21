#!/usr/bin/sh

#***************************#
#	DRUSTROYER INSTALLER	#
#							#
#	Fernando C.G.			#
#							#
#	Este cuadro no dice		#
#	nada importante, pero	#
#	es un buen cliche...	#
#***************************#

function instalador(){
	sudo pip install requests 
	sudo pip install requesocks
	sudo pip install requests[socks]
	sudo pip install ansicolors
	sudo pip install untangle
	sudo pip install BeautifulSoup 
	sudo pip install bs4
	echo "CREANDO DIRECTORIO /opt/drustoyer"
	sudo mkdir -pm 755 /opt/drustroyer
	echo "CREANDO DIRECTORIO PARA USUARIO..."
	sudo mkdir -pm 711 ~/.drustroyer
	echo "Moviendo archivos necesarios a /opt/drustroyer"
	sudo cp ./* /opt/drustroyer
	cd /opt/drustroyer/config/generadores
	echo "CREANDO LA BASE DE DATOS, ESTO PUEDE TOMAR MUCHO TIEMPO, PUEDE IN POR UN CAFE :)"
	sudo sqlite3 drupal_vuln.db < drupal_vuln.sql
	sudo python fill_db.py
}

if [ -d /opt/drustroyer ];
then
	echo "Ya se encuentra instalado en el equipo"
else
	if [ $(grep debian /etc/*release|wc -l) ] || [ $(grep kali /etc/*release|wc -l) ];
	then
		sudo apt-get update
		sudo apt-get install -y python-pip tor sqlite3
		instalador
	elif [ $(grep Ubuntu /etc/*release) ];
	then
		if [ $(lsb_release -a|grep precise|wc -l) ];
		then
			deb http://deb.torproject.org/torproject.org precise main
			deb-src http://deb.torproject.org/torproject.org precise main
		elif [ $(lsb_release -a|grep trusty|wc -l) ];
		then 
			deb http://deb.torproject.org/torproject.org trusty main
			deb-src http://deb.torproject.org/torproject.org trusty main
		elif [ $(lsb_release -a|grep trusty|wc -l) ]; 
		then
			deb http://deb.torproject.org/torproject.org xenial main
			deb-src http://deb.torproject.org/torproject.org xenial main
		else 
			echo "No se puede instar TOR en este equipo..."
		fi
		sudo apt-get update
		sudo apt-get install -y python-pip tor sqlite3 deb.torproject.org-keyring
		instalador
	elif [ $(grep fedora /etc/*release|wc -l) ] || [ $(grep centos /etc/*release|wc -l) ];
	then
		sudo wget https://www.torproject.org/dist/tor-0.2.8.9.tar.gz
		sudo tar xzf tor-0.2.8.9.tar.gz; 
		cd tor-0.2.8.9
		sudo ./configure && make
		cd ..
		sudo rm -rf tor-0.2.8.9
		sudo yum install -y python-pip sqlite3
		instalador
	else
		echo "La herramienta no soporta tu distribucion, aun..."
	fi
fi