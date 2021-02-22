class UltimoDiaMes:
    @staticmethod    
    def ultimo_dia_mes(mes, ano):
        meses_31_dias = ["01", "03", "05", "07", "08", "10", "12"]
        
        if mes == "02":
            if int(ano) % 4 == 0:
                return "29"
            else:
                return "28"
        elif mes in meses_31_dias:
            return "31"
        else:
            return "30" 