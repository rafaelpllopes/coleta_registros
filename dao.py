#! python3
# -*- coding: utf-8 -*-
from database import Database
from helpers.obter_ultimo_dia_mes import UltimoDiaMes

class RegistradosDAO(Database):
    def __init__(self):
        super().__init__()
        
    def inserir_registros(self, registros: []):
        """
            registros = [
                (ponto, matricula, registro)
            ]
        """
        try:
            for registro in registros:
                self.cursor.execute(f"INSERT INTO HE22 VALUES(NULL,'{registro[0]}','{registro[1]}','0','0','0','2','0','4','255','1','{registro[2]}','0','0','4','0','0')")
                self.conn.commit()
        except Exception as erro:
            print(erro)
            
    def verifica_existencia_registro(self, matricula, mes, ano):
        try:
            ultimo_dia_mes = UltimoDiaMes.ultimo_dia_mes(mes, ano)
            sql = f"SELECT HE22_ST_MATRICULA AS matricula, HE22_DT_REGISTRO as registro FROM HE22 WHERE HE22_ST_MATRICULA = '{matricula}' AND HE22_DT_REGISTRO BETWEEN '{ano}-{mes}-01 00:00:00' AND '{ano}-{mes}-{ultimo_dia_mes} 23:59:59'"
            dados = self.cursor.execute(sql)
            
            resultados = dados.fetchallmap()
            
            registros = []        
            
            for resultado in resultados:
                registros.append({ "matricula": resultado['MATRICULA'], "registro": resultado['REGISTRO'].strftime('%d/%m/%Y %H:%M') })
                    
            return registros
            
        except Exception as erro:
            print(erro)
            
if __name__ == '__main__':
    pass