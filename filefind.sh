#!/bin/bash

#Fazer um google dork para encontrar arquivos e  paginas do alvo com a extenção escolhida

if [ "$1" == "" ]
then
		echo "Redteam - File find"
		echo "modo de uso: $0 dominio + extenção do arquivo"
		echo "Exemplo: $0 site.com.br pdf"
		echo "Extenções aceitas: pdf, xml, docx, xlsx, pptx, doc, ppt, xls "
else
	echo "##########R3dT34M T00ls - File Find#######"
	echo "author: 0xsl4p"

	lynx --dump "https://google.com/search?&q=site:$1+ext:$2" | grep ".$2" | cut -d "=" -f2 | egrep -v "site|google" | sed 's/...$//'g

fi