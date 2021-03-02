#! python3
# -*- coding: utf-8 -*-
import re
from os import listdir
from helpers.remove_files import RemoveFiles
from helpers.obter_nome_arquivo_rep import ObterNomeArquivoREP
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
        
    def _filtrar_registros(self, rep, mes, ano):
        rep_arq = f'downloads/{rep}'            
        registros_inserir = []
        registro_existentes = self.dao.obter_registro_por_ponto_mes_ano(self.ponto, mes, ano)
        
        print(f"Filtrando os registros {mes}/{ano}")
        with open(rep_arq) as arquivo:
            rep = arquivo.read()
            for servidor in self.servidores:
                registros = re.findall(r'(?:\d{10})(\d{2})(%s)(%s)(\d{2})(\d{2})(%s)(?:.{4,})' % (mes, ano, servidor['pis']), rep)
                
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
                                
        return registros_inserir
           
    def _obtem_mes_ano_anterior(self, mes, ano):
        if mes == '01':
            mes = '12'
            ano = str(int(ano) - 1)
            return (mes, ano)

        mes = str(int(mes) - 1).zfill(2)
        
        return (mes, ano)  
    
    def inserir_registros(self, mes, ano):
        nome_arquivo_rep = ObterNomeArquivoREP.nome_arquivo(self.rep)
        
        if not nome_arquivo_rep:
            return
        
        ultimo_mes, ultimo_ano = self._obtem_mes_ano_anterior(mes, ano)
        penultimo_mes, penultimo_ano = self._obtem_mes_ano_anterior(ultimo_mes, ultimo_ano)
        
        registros = [
            *self._filtrar_registros(nome_arquivo_rep, penultimo_mes, penultimo_ano), 
            *self._filtrar_registros(nome_arquivo_rep, ultimo_mes, ultimo_ano), 
            *self._filtrar_registros(nome_arquivo_rep, mes, ano)
        ]
                
        if registros:
            self.dao.inserir_registros(registros)
            print(f"Registros {self.rep} inseridos com sucesso .")
        else:
            print(f"Não há registros para serem inseridos do registrador {self.rep}")

if __name__ == '__main__':
    pass