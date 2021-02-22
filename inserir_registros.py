#! python3
# -*- coding: utf-8 -*-
from json import load
from datetime import date
from inserir_db import InserirDB

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
            mes = data_atual.month()
            ano = data_atual.year()
            
            inserir.inserir_registros(mes, ano)
        except Exception as error:
            print(error)
    
if __name__ == '__main__':
    main()