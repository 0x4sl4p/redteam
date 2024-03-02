#!/usr/bin/env python3

import argparse
import requests
import os
import subprocess
import time

# Função para exibir o banner
def exibir_banner():
    banner = """
  ██████╗ ██████╗ ██╗   ██╗██████╗ ██╗████████╗███████╗██████╗ 
 ██╔═══██╗██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝██╔════╝██╔══██╗
 ██║   ██║██████╔╝██║   ██║██║  ██║██║   ██║   █████╗  ██████╔╝
 ██║▄▄ ██║██╔═══╝ ██║   ██║██║  ██║██║   ██║   ██╔══╝  ██╔══██╗
 ╚██████╔╝██║     ╚██████╔╝██████╔╝██║   ██║   ███████╗██║  ██║
  ╚══▀▀═╝ ╚═╝      ╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                    CSIRT - feito por sl4p
    """
    print(banner)

# Função para fazer dump do processo com o Volatility
def fazer_dump(pid, caminho_saida):
    print(f"Fazendo dump do processo PID {pid}...")
    comando = f"vol.py -f '{args.memoria}' --profile={args.profile} --dump-dir={caminho_saida} procdump -p {pid}"
    subprocess.run(comando, shell=True)
    print(f"Dump do processo PID {pid} concluído.")

# Função para definir permissões de arquivo
def definir_permissao_arquivo(arquivo):
    os.chmod(arquivo, 0o644)  # Permissão de leitura para todos os usuários

# Função para enviar arquivo para análise no VirusTotal
def enviar_arquivo_virustotal(apikey, arquivo):
    print(f"Enviando arquivo {arquivo} para análise ao VirusTotal...")
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': apikey}
    files = {'file': (os.path.basename(arquivo), open(arquivo, 'rb'))}
    response = requests.post(url, files=files, params=params)
    if response.status_code == 200:
        print("Arquivo enviado com sucesso.")
        return response.json()
    else:
        print(f"Erro ao enviar arquivo para análise: {response.text}")
        return None

# Função para obter informações do arquivo através do VirusTotal
def obter_informacoes_virustotal(apikey, resource):
    print(f"Obtendo informações do VirusTotal para o arquivo com hash {resource}...")
    url = f'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': apikey, 'resource': resource}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Informações do VirusTotal obtidas para o arquivo com hash {resource}.")
        return response.json()
    else:
        print(f"Erro ao obter informações do VirusTotal: {response.text}")
        return None

# Função para gerar relatório de resultados em arquivo de texto
def gerar_relatorio_txt(relatorio, caminho_saida):
    nome_arquivo = f"{caminho_saida}/{relatorio['PID']}.txt"
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(f"PID: {relatorio['PID']}\n")
        arquivo.write(f"Tamanho: {relatorio['Tamanho']}\n")
        arquivo.write(f"SHA256: {relatorio['SHA256']}\n")
        arquivo.write(f"Tipo: {relatorio['Tipo']}\n")
        arquivo.write(f"Estatísticas da última análise: {relatorio['Estatísticas da última análise']}\n")

# Parseador de argumentos
parser = argparse.ArgumentParser(description="Script para fazer dump de processos com Volatility e enviar para análise no VirusTotal.")
parser.add_argument("-p", "--memoria", help="Caminho para o arquivo de memória a ser analisado pelo Volatility", required=True)
parser.add_argument("-o", "--output", help="Diretório onde os dumps dos processos serão salvos", required=True)
parser.add_argument("-w", "--relatorio", help="Diretório onde os relatórios do VirusTotal serão salvos", required=True)
parser.add_argument("-k", "--apikey", help="Chave de API do VirusTotal", required=True)
parser.add_argument("-pr", "--profile", help="Perfil da memória para o Volatility", required=True)

args = parser.parse_args()

# Exibir banner
exibir_banner()

# Comando para listar os PIDs usando o vol.py e awk
comando_pids = f"vol.py -f '{args.memoria}' --profile={args.profile} pslist | awk 'NR>1 {{print $3}}' | grep -oE '[0-9]+'"

# Executar o comando para obter os PIDs
saida_pids = subprocess.check_output(comando_pids, shell=True)
pids = saida_pids.decode('utf-8').splitlines()

# Caminho para salvar os arquivos de dump
caminho_saida_dump = args.output
# Criar pasta para salvar os relatórios do VirusTotal
caminho_relatorios_vt = args.relatorio
if not os.path.exists(caminho_relatorios_vt):
    os.makedirs(caminho_relatorios_vt)

# Realiza o dump do processo para cada PID
for pid in pids:
    fazer_dump(pid, caminho_saida_dump)

# Define permissões de arquivo para todos os arquivos no diretório de saída
for arquivo in os.listdir(caminho_saida_dump):
    definir_permissao_arquivo(os.path.join(caminho_saida_dump, arquivo))

# Lista de arquivos gerados
arquivos_dump = [os.path.join(caminho_saida_dump, arquivo) for arquivo in os.listdir(caminho_saida_dump) if arquivo.endswith(".exe")]

# Lista para armazenar os relatórios de cada arquivo
relatorios = []

# Enviar cada arquivo para análise no VirusTotal e obter informações sobre eles
for arquivo in arquivos_dump:
    nome_arquivo = os.path.basename(arquivo)
    print(f"Enviando arquivo {nome_arquivo} para análise ao VirusTotal...")
    resp_envio = enviar_arquivo_virustotal(args.apikey, arquivo)
    if resp_envio and 'resource' in resp_envio:
        resource = resp_envio['resource']
        print(f"Hash do arquivo: {resource}")
        print("Aguardando resultados da análise...")
        informacoes_arquivo = obter_informacoes_virustotal(args.apikey, resource)
        if informacoes_arquivo:
            # Adiciona as informações do arquivo ao relatório
            relatorio = {'PID': pid, 'Tamanho': informacoes_arquivo.get('file_size'), 'SHA256': informacoes_arquivo.get('sha256'),
                         'Tipo': informacoes_arquivo.get('type'), 'Estatísticas da última análise': informacoes_arquivo.get('scans')}
            relatorios.append(relatorio)
            time.sleep(15)  # Intervalo de espera de 15 segundos entre cada solicitação

# Salva os relatórios em arquivos de texto na pasta de relatórios do VirusTotal
for relatorio in relatorios:
    gerar_relatorio_txt(relatorio, caminho_relatorios_vt)

print(f"Relatórios salvos com sucesso na pasta de relatórios do VirusTotal.")
