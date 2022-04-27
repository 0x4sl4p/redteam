#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, os
import subprocess
import argparse
import shutil
from datetime import datetime
import pyscreenshot as ImageGrab
import pyfiglet

#Autor 0xsl4p
#Ferramenta para automatizar testes iniciais em pentest interno

ascii_banner = pyfiglet.figlet_format("R3DTEAM SOFTWALL TOOLS - \n First Infra \n sl4p", font = "digital")
print(ascii_banner)

PROG_VERS='1.0'
PROG_DATE='16/04/2022'

comandos=[
	[['ifconfig'],3, "IP Recebido automáticamente"],
	[['route'],3, "Rotas recebidas automáticamente"],
	[['arp', '-nv'],3, "Tabela ARP"],
	[['cat','/etc/resolv.conf'],3,"DNS recebido automáticamente"],
	[['traceroute','-n','--max-hops=15','www.google.com.br'],3, "Rota de saída até Google"],				
	[['ping', '-c6','8.8.8.8'],3, "Comando PING para servidor DNS Google"],
	[['ping', '-c6','google.com'],3, "Comando PING para site Google"],
	[['curl', 'ifconfig.me/all'],3,"IP de saída para internet"],
]
comandosComTempo=[
	[['wget', 'ftp://ftp.adobe.com/pub/adobe/reader/win/AcrobatDC/1901220034/AcroRdrDC1901220034_en_US.exe', '-O','/tmp/AcrobatDC.exe'],10,"Download de arquivo Executavel"],
	[['nc', '-v', 'google.com', '80'],3,"Acesso Web externo"],
	[['nc', '-v', 'ftp.br.debian.org', '21'],5,"Acesso a servidor FTP externo"],
	[['wget', 'http://ftp.br.debian.org/debian-cd/10.0.0-live/amd64/iso-hybrid/debian-live-10.0.0-amd64-cinnamon.iso','-t','2','-O','/tmp/debian.iso'],20,"Download de arquivo sem contrle de throughput"],
	[['nc', '-v', 'scanme.nmap.org', '22'],5,"Acesso a servidor SSH externo"],
	[['netdiscover'], 120,"ARP scan utilizando ferramenta netdiscovery" ]
]

def parse_args():
	parser = argparse.ArgumentParser(
		prog = 'First Infra recon', 
		description = 'Automatização dos testes iniciais',
		add_help=False,
		epilog = '''          Exemplos: python3 '''+sys.argv[0] +' <Nome_do_Cliente>'
		)
	parser.add_argument("-h", "--help", action="help", help="Exibe esta mensagem de ajuda")
	parser.add_argument('-v','--version', action='version', version = "%(prog)s V"+PROG_VERS+' '+PROG_DATE, help = 'Exibe a versão do programa')
	parser.add_argument('-q','--quiet', action='store_false', help = 'Não exibe o banner ao iniciar o programa')
	parser.add_argument('-c','--client', metavar='', default="_screenshots", help='Nome do cliente/projeto. [ Def: %(default)s ]')
	parser.add_argument('-t','--type', metavar='', default="infra", choices=['infra','web', 'all'], help='Tipo de teste a ser efetuado. [ Def: %(default)s ]')
	parser.add_argument('-f','--format', metavar='', default="jpeg", help='Formato de saída das imagens. [ Def: %(default)s ]')
	# parser.add_argument('', '', default = '', help = '')
	return parser.parse_args()

def mkdirClient(clientDir):
    '''
    Create output directories
    '''
    if not os.path.exists(clientDir):
        os.makedirs(clientDir)
    else:
    	if os.path.exists(clientDir+"_1"):
    		shutil.rmtree(clientDir+"_1")
    	os.rename(clientDir, clientDir+"_1")
    	os.makedirs(clientDir)

def screenshot(dirname,name,formatImg):
	imagem=ImageGrab.grab()
	# imagem.save(dirname+'/'+str(time.time()*1000.0)+'.'+formatImg+, formatImg)
	imagem.save(dirname+'/'+str(name)+'.'+formatImg, formatImg)
	
def runCmd():
	try:
		for cmd in comandos:
			subprocess.call(['clear'], shell=True)
			sep()
			print("root# "+str(cmd[0])+"\n")
			subprocess.call(cmd[0])
			screenshot(args.client,cmd[2],args.format)
			time.sleep(cmd[1])
	except(KeyboardInterrupt):
		print("\r\n")
		sys.exit()
		time.sleep(1)

def runCmdTime():
	try:
		for cmdTime in comandosComTempo:
			subprocess.call(['clear'], shell=True)
			sep()
			pt=subprocess.Popen(cmdTime[0], shell=False, stdin=subprocess.PIPE , stderr=subprocess.STDOUT)
			time.sleep(cmdTime[1])
			screenshot(args.client,cmdTime[2],args.format)
			pt.terminate()
			time.sleep(2)
	except(KeyboardInterrupt):
			print("\r\n")
			sys.exit()
			time.sleep(1)

def sep():
	head='='*100+"\n"
	head+='='*100+"\n"
	print(head)
#############################################################################
def main():
	try:	
		os.system('cls' if os.name == 'nt' else 'clear')
		if args.quiet:
			print(ascii_banner)
			time.sleep(4)
		mkdirClient(args.client)
		if args.type == "infra":
			runCmd()
			runCmdTime()
		elif args.type == "web":
			print("web")
		elif args.type == "all":
			print('all')
		else:
			print("Você deve selecionar uma opção de scann válida: ['infra','web', 'all']")
	except(KeyboardInterrupt):
		print(CVm_+"Saindo.........\r\n")
		sys.exit()
		sleep(2)

if __name__ == "__main__" :
		args = parse_args()
		main()


