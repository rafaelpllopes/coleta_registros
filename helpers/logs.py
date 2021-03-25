class Logs:
    @staticmethod
    def info(tipo: str, mensagem: str):
        with open("logs.txt", "a") as logs:
            logs.write(f"{tipo} - {mensagem}\n")
        
if __name__ == '__main__':
    pass
    