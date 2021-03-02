#! python3
# -*- coding: utf-8 -*-
from json import load
from datetime import date
from inserir_db import InserirDB
from helpers.remove_files import RemoveFiles
from helpers.obter_nome_arquivo_rep import ObterNomeArquivoREP
from sys import argv
from os import listdir
from re import search

registradores = []

with open('equipamentos.json', 'r') as arquivo:
    registradores = load(arquivo)

def inserir_todos():
    for registrador in registradores():
        try:
            rep = registrador['rep']
            ponto = registrador['codigo_db']
            inserir = InserirDB(rep, ponto)
            
            data_atual = date.today()
            mes = str(data_atual.month).zfill(2)
            ano = str(data_atual.year)
            
            inserir.inserir_registros(mes, ano)
        except Exception as error:
            print(error)
    
    RemoveFiles.remove_all()
def inserir_por_rep(rep):
    for registrador in registradores:
        if rep == registrador['rep']:
            try:
                print(registrador['local'])
                rep = registrador['rep']
                ponto = registrador['codigo_db']
                inserir = InserirDB(rep, ponto)
                
                data_atual = date.today()
                mes = str(data_atual.month).zfill(2)
                ano = str(data_atual.year)
                
                inserir.inserir_registros(mes, ano)
                file = ObterNomeArquivoREP.nome_arquivo(rep)
                RemoveFiles.remove_one(file)
            except Exception as error:
                pass
            break
                
if __name__ == '__main__':
    try: 
        rep = argv[1]
        inserir_por_rep(rep)
    except:
        arquivos = listdir('downloads')
        for arquivo in arquivos:
            rep = search(r'(\w+)?(\d{17})(\.txt)?', arquivo)
            if rep:
                inserir_por_rep(rep.group(2))
            
            