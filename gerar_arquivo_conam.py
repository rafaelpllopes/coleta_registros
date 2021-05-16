from dao import RegistradosDAO

def gerar_txt(periodo_incial, periodo_final):
    try:
        with open('saude.txt', 'w') as arq:
            registros = RegistradosDAO()
            resultados = registros.obter_registros_por_mes_ano(periodo_incial, periodo_final)
            # {'matricula': '00000000000000020843', 'ponto': 147, 'registro': '10/05/2021 05:48'}
            for resultado in resultados:
                data_time = str(resultado['registro']).split(' ')
                dia, mes, ano = data_time[0].split('/')
                hora, minuto = data_time[1].split(':')
                # print('    {} {} {} {} {} {}\r\n'.format(dia, mes, ano, hora, minuto, resultado['matricula'][14:]))
                arq.write('    {} {} {} {} {} {}\r\n'.format(dia, mes, ano, hora, minuto, resultado['matricula'][14:]))
    except Exception as erro:
        print(f'Erro: {erro}')

if __name__ == '__main__':
    periodo_incial = { 'mes': '01', 'ano': '2021'}
    periodo_final = { 'mes': '12', 'ano': '2021'}
    gerar_txt(periodo_incial, periodo_final)