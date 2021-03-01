#! python3
# -*- coding: utf-8 -*-
from json import load
from datetime import date
from inserir_db import InserirDB
from helpers.remove_files import RemoveFiles
from sys import argv

def registradores():
    registradores = []

    with open('equipamentos.json', 'r') as arquivo:
        registradores = load(arquivo)
    
    return registradores

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

def inserir_por_local(local):
    for registrador in registradores():
        if local.lower() in registrador['local'].lower() or local == registrador['rep']:
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
            break
                
if __name__ == '__main__':
    try: 
        local = argv[1]
        inserir_por_local(local)
    except:
        pass
        inserir_todos()