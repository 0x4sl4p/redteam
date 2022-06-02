#!/bin/bash

#Criar um script para baixar arquivos com google dork e usar oexiftools para extrair os metadados

if [ "$1" == "" ]
then
		echo "Redteam - metadados extract"
		echo "modo de uso: $0 dominio + extenção do arquivo"
		echo "Exemplo: $0 site.com.br pdf"
		echo "Extenções aceitas: pdf, xml, docx, xlsx, pptx, doc, ppt, xls "
else
	echo "##########R3dT34M T00ls - Metadados Extract#######"
	echo "author: 0xsl4p"

	lynx --dump "https://google.com/search?&q=site:$1+ext:$2" | grep ".$2" | cut -d "=" -f2 | egrep -v "site|google" | sed 's/...$//' > $1.txt


	for url in $(cat $1.txt)
do
	wget -q $url
done
	
	exiftool *.$2
fi