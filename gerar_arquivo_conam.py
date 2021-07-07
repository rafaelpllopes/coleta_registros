from dao import RegistradosDAO
from helpers.obter_mes_ano_anterior import ObterUltimoMesAnoAnterior
from datetime import date
import os

""" 
    Caminho onde deve ser salvo o arquivo.
    export PATH_SAUDE=
"""
PATH_ARQ = os.getenv("PATH_SAUDE") 

def gerar_txt(periodo_incial, periodo_final):
    """ 
        Função responsavel por gerar o arquivo, atraves de consulta ao banco de dados.
        Deve receber os dicionarios com as das iniciais e finais no formato:
        { 'mes': '##', 'ano': '####', }
    """
    try:
        with open(f'{PATH_ARQ}/saude.txt', 'w') as arq:
            registros = RegistradosDAO()
            resultados = registros.obter_registros_por_mes_ano(periodo_incial, periodo_final)
            for resultado in resultados:
                data_time = str(resultado['registro']).split(' ')
                dia, mes, ano = data_time[0].split('/')
                hora, minuto = data_time[1].split(':')
                arq.write('    {} {} {} {} {} {}\r\n'.format(dia, mes, ano, hora, minuto, resultado['matricula'][14:]))
    except Exception as erro:
        print(f'Erro: {erro}')

if __name__ == '__main__':
    data_atual = date.today() # pega a data atual
    mes = str(data_atual.month).zfill(2) # pega o mes atual e insere um zero a esquerda para data menor que 2 digitos
    ano = str(data_atual.year) # pega o ano atual
    mes_anterior, ano_anterior = ObterUltimoMesAnoAnterior.obter_mes_ano_anterior(mes, ano) # traz mes ano anterior
    periodo_incial = { 'mes': mes_anterior, 'ano': ano_anterior } # gera o dicionario que será usado na função
    periodo_final = { 'mes': mes, 'ano': ano }
    gerar_txt(periodo_incial, periodo_final)