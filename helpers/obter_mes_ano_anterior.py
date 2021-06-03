class ObterUltimoMesAnoAnterior:    
    @staticmethod
    def obter_mes_ano_anterior(mes, ano):
        if mes == '01':
            mes = '12'
            ano = str(int(ano) - 1)
            return (mes, ano)

        mes = str(int(mes) - 1).zfill(2)
        
        return (mes, ano)  