#!/bin/sh

#***************************#
#	druspawn INSTALLER	#
#							#
#	Fernando C.G.			#
#							#
#	Este cuadro no dice		#
#	nada importante, pero	#
#	es un buen cliche...	#
#***************************#

sudo rm -rf /opt/drustroyer
for dir in /home/*/
do
	sudo rm -rf $dir.drustroyer
done
sudo rm -rf /root/.drustroyer
sudo rm -rf /bin/drustroyer

sudo rm -rf /opt/druspawn
for dir in /home/*/
do
	sudo rm -rf $dir.druspawn
done
sudo rm -rf /root/.druspawn
sudo rm -rf /bin/druspawn

echo "DruSpawn desinstalado de manera exitosa..."
