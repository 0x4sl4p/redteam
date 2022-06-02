#!/bin/bash
#criar um script para baixar o index e filtrar o os links no codigo e encontrar o ip de cada link
if [ "$1" == "" ]
then
		echo "Redteam - Parsing HTML"
		echo "modo de uso: $0 dominio"
		echo "Exemplo: $0 businesscorp.com.br"
else
	echo "################PARSING REDTEAM BASH####################################"
	wget $1
	cat index.html | grep "href" | grep "\." | cut -d "/" -f 3 | cut -d '"' -f 1 | grep -v "<li" > lista.txt
	for host in  $(cat lista.txt); 
	   do host $host | grep -v "NXDOMAIN" | cut -d " " -f 1,4 >> $1.txt;

	done
	cat $1.txt
fi