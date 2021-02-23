#! python3
# -*- coding: utf-8 -*-
from json import load
from datetime import date
from inserir_db import InserirDB
from helpers.remove_files import RemoveFiles

def registradores():
    registradores = []

    with open('equipamentos.json', 'r') as arquivo:
        registradores = load(arquivo)
    
    return registradores

def main():
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
    
if __name__ == '__main__':
    main()