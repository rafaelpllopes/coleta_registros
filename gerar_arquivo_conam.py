from dao import RegistradosDAO
from helpers.obter_mes_ano_anterior import ObterUltimoMesAnoAnterior
from datetime import date

def gerar_txt(periodo_incial, periodo_final):
    try:
        with open('saude.txt', 'w') as arq:
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
    data_atual = date.today()  
    mes = str(data_atual.month).zfill(2)
    ano = str(data_atual.year)
    mes_anterior, ano_anterior = ObterUltimoMesAnoAnterior.obter_mes_ano_anterior(mes, ano)
    periodo_incial = { 'mes': mes_anterior, 'ano': ano_anterior }
    periodo_final = { 'mes': mes, 'ano': ano }
    gerar_txt(periodo_incial, periodo_final)