#! python3
from coleta_registros import FirefoxColeta, ChromeColeta
from json import load
import subprocess

def coletar(registradores):
    mensagem = ''

    for registrador in registradores:
        mensagem = f"Coletado os registros da unidade {registrador['local']}, ip {registrador['ip']}: "
        
        ping = subprocess.run(["ping", "-c", "1", f"{registrador['ip']}"], stdout=subprocess.PIPE)
        resposta = ping.stdout.decode('UTF-8') if ping.returncode == 0 else ''
        if not resposta:
            continue
            
        try:
            if registrador['equipamento'] == 'Henry Prisma':
                coletar = FirefoxColeta(
                    f"http://{registrador['ip']}", registrador['user'], registrador['pass'])
                coletar.coleta_registros_registrador_henry()
            else:
                coletar = FirefoxColeta(
                    f"https://{registrador['ip']}", registrador['user'], registrador['pass'])
                coletar.coleta_registros_registrador_controlId()
            
            mensagem += "OK"
        except Exception as erros:
            mensagem += f'{erros}'
        
        print(mensagem)

def main():
    
    registradores = []

    with open('equipamentos.json', 'r') as arquivo:
        registradores = load(arquivo)

    coletar(registradores)


if __name__ == '__main__':
    main()
