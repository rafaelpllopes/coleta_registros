#! python3
# -*- coding: utf-8 -*-
from database import Database

class RegistradosDAO(Database):
    def __init__(self):
        super().__init__()
        
    def inserir_registros(self, registros: []):
        try:
            self.cursor.executemany("INSERT INTO HE22 VALUES(NULL,'?','?','0','0','0','2','0','4','255','1','?','0','0','4','0','0')", registros)
            self.conn.commit()
        except Exception as erro:
            print(erro)
            
    def verifica_existencia_registro(self):
        pass
            
if __name__ == '__main__':
    pass