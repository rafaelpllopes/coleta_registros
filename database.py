#! python3
# -*- coding: utf-8 -*-
import fdb
from json import load

config = []

with open('db_config.json', 'r') as arq:
    config = load(arq)

class Database:
    def __init__(self):
        self._conn = fdb.connect(dsn=f"{config['host']}:{config['database']}", user=config['user'], password=config['password'], charset='UTF8')
    
    @property
    def cursor(self):
        return self._conn.cursor()
    
    def destroy(self):
        self._conn.close()

if __name__ == "__main__":
    pass
    