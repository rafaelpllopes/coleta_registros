from os import listdir
from re import search

class ObterNomeArquivoREP:
    @staticmethod
    def nome_arquivo(rep):  
        print(f"Verificando existencia do arquivo rep do registrador {rep}")
        nome_arquivo = ''
        arquivos = listdir('downloads')
        
        if not arquivos:
            return nome_arquivo
        
        for arquivo in arquivos:
            existe = search(r'([A-Za-z]{2,})?(\_)?(%s)(.txt)$' % rep, arquivo)
            if existe:
                nome_arquivo = existe.group()
        
        return nome_arquivo
        
if __name__ == '__main__':
    pass