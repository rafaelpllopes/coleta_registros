#! python3
# -*- coding: utf-8 -*-
import re
from os import listdir
from helpers.remove_files import RemoveFiles
from dao import RegistradosDAO

class InserirDB:
    def __init__(self, rep, ponto_db):
        self._rep = rep
        self._ponto = ponto_db
        self._servidores = self.obter_servidores()
        self._dao = RegistradosDAO()
    
    @property
    def rep(self):
        return self._rep
    
    @property
    def ponto(self):
        return self._ponto
        
    @property
    def servidores(self):
        return self._servidores

    @property
    def dao(self):
        return self._dao
    
    def obter_servidores(self):
        resultados = []
        with open('rep_colaborador.txt', 'r') as arquivo:
            servidores = []
            for linha in arquivo:
                servidores.append(re.search(r'(?:\d\+\d\+\w\[)(\d{12})(?:\[)(.+)(?:\[\d\[\d\[)(\d+)', linha.replace('\n', '')))
        for servidor in servidores:
            resultados.append({ 'nome' : servidor.group(2), 'pis' : servidor.group(1).zfill(12), 'matricula': servidor.group(3).zfill(20) })
        
        return resultados
        
    def _filtrar_registros(self, mes, ano):
        print("Filtrando os registros")
        registros_inserir = []
        nome_arquivo_rep = self._nome_arquivo(self.rep)
        registro_existentes = self.dao.obter_registro_por_ponto_mes_ano(self.ponto, mes, ano)
        
        if not nome_arquivo_rep:
            print(f"{self.rep} não esta na pasta.")
            return
        
        with open(f'downloads/{nome_arquivo_rep}') as arquivo:
            rep = arquivo.read()
            for servidor in self.servidores:
                registros = re.findall(r'(?:\d{10})(\d{2})(%s)(%s)(\d{2})(\d{2})(%s)(?:.{4})' % (mes, ano, servidor['pis']), rep)               
                if registros:
                    if registro_existentes:
                        for reg in registro_existentes:
                            data = reg['registro'].split(' ')
                            dia, mes, ano = data[0].split('/')
                            hora, minuto = data[1].split(':')
                            dado_comparar = (dia.zfill(2), mes.zfill(2), ano, hora.zfill(2), minuto.zfill(2), servidor['pis'])
                            if dado_comparar in registros:
                                registros.remove(dado_comparar)
                    
                    for registro in registros:
                        registros_inserir.append((self.ponto, servidor['matricula'], f"{registro[2]}-{registro[1]}-{registro[0]} {registro[3]}:{registro[4]}"))
                        
        RemoveFiles.remove_one(nome_arquivo_rep)
        
        return registros_inserir
    
    def _nome_arquivo(self, rep):  
        print(f"Verificando existencia do arquivo rep do registrador {rep}")  
        nome_arquivo = ''
        for arquivo in listdir('downloads'):
            existe = re.search(r'([A-Za-z]{2,})?(%s)(.txt)$' % rep, arquivo)
            if existe:
                nome_arquivo = existe.group()
        
        return nome_arquivo
        
    def inserir_registros(self, mes, ano):
        
        registros = self._filtrar_registros(mes, ano)
        if registros:
            self.dao.inserir_registros(registros)
            print(f"Registros {self.rep} inseridos com sucesso.")
        else:
            print(f"Não há registros para serem inseridos do registrador {self.rep}")       

if __name__ == '__main__':
    pass