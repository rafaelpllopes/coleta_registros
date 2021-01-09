#! python3

from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
from time import sleep
from abc import ABC
import os

class ColetarRegistros(ABC):
    def __init__(self, url, usuario, senha, browser):
        """
            * Essa classe não pode ser implementada diretamente, somente pelas classes filhas
            Coleta_Registros, classe com metodos para coletar os registros do ponto, de acordo com a URL
                - browser: instancia do navegador que vem da classe filha
                - url: endereço da pagina do registrador de ponto para acesso
                - usuario: nome do usuario para logar
                - senha: do usuario para logar
        """
        self.__browser = browser
        self.__url = url
        self.__usuario = usuario
        self.__senha = senha

    @property
    def url(self):
        return self.__url

    @property
    def usuario(self):
        return self.__usuario

    @property
    def senha(self):
        return self.__senha

    @property
    def browser(self):
        return self.__browser
    
    def __get_periodos_coleta(self, set_hour=True):
        
        inicio = f"01/{str(int(datetime.now().strftime('%m'))).zfill(2)}/{datetime.now().strftime('%Y')}"
        fim = f"{datetime.now().strftime('%d')}/{datetime.now().strftime('%m')}/{datetime.now().strftime('%Y')}"
        
        if set_hour:
            inicio = f"01/{str(int(datetime.now().strftime('%m'))).zfill(2)}/{datetime.now().strftime('%y')} 00:00"
            fim = f"{datetime.now().strftime('%d')}/{datetime.now().strftime('%m')}/{datetime.now().strftime('%y')} 23:59"
        
        return {
            "inicio": inicio,
            "fim": fim
        }
    
    def __verifica_termino_download(self):
        sleep(1)        
        arq = os.listdir("/home/info/Dev/converte_comunica_ponto")
        return ".part" in arq or ".crdownload" in arq

    def coleta_registros_registrador_henry(self):
        try:
            self.browser.get(self.url)  # Abre a pagina do registrador de ponto

            # Selecio os campos e preenche para realizar login
            site_login = self.browser.find_element_by_id('lblLogin')
            site_senha = self.browser.find_element_by_id('lblPass')
            botao_entrar = self.browser.find_element_by_tag_name('a')
            site_login.send_keys(self.usuario)
            site_senha.send_keys(self.senha)
            botao_entrar.click()

            # Clica no menu eventos
            menu_events = self.browser.find_element_by_id('divMenuEvents')
            menu_events.click()

            # Clica no menu filtro
            opcao_filtro_por_data = self.browser.find_element_by_id(
                'menuItem2')
            opcao_filtro_por_data.click()
            
            periodos = self.__get_periodos_coleta()
                        
            # Seleciona os campos de data de clica para download
            self.browser.execute_script(
                f"document.querySelector('#lblDataI').value = '{periodos['inicio']}'")
            self.browser.execute_script(
                f"document.querySelector('#lblDataF').value = '{periodos['fim']}'")

            sleep(5)
            botao_baixar = self.browser.find_elements_by_css_selector(
                '#communication table a')
            botao_baixar[0].click()

            terminou = self.__verifica_termino_download()
            tentativas = 0
            while terminou or tentativas < 60:
                tentativas += 1
                terminou = self.__verifica_termino_download()
            
            sleep(3)
            botao_sair = self.browser.find_element_by_id('exitBtn')
            botao_sair.click()
                                    
            self.browser.quit()

        except Exception as erros:
            # print(f'Erros: {erros}')
            self.browser.quit()
            raise NameError('FALHA')

    def coleta_registros_registrador_controlId(self):
        try:
            self.browser.get(self.url)
            usuario_input = self.browser.find_element_by_id('input_user')
            senha_input = self.browser.find_element_by_id('input_password')
            btn_logar = self.browser.find_element_by_id('logar')
            usuario_input.send_keys(self.usuario)
            senha_input.send_keys(self.senha)
            btn_logar.click()
            
            sleep(5)
            menu_afd = self.browser.find_element_by_css_selector('#MasterPage_menu ul li:nth-child(4) a')
            menu_afd.click()
            
            sleep(1)
            por_data = self.browser.find_element_by_css_selector('a[modal="afd_data"]')
            por_data.click()
            
            periodos = self.__get_periodos_coleta(False)
            
            sleep(5)
            self.browser.execute_script(f"document.querySelector('#initial_date').value = '{periodos['inicio']}'")
            sleep(1)
            download = self.browser.find_element_by_css_selector('.modal-footer button[class="btn green"]')
            download.click()
                       
            terminou = self.__verifica_termino_download()
            tentativas = 0
            while terminou or tentativas < 60:
                tentativas += 1
                terminou = self.__verifica_termino_download()
                
            self.browser.quit()
        except Exception as erros:
            # print(f'Erros: {erros}')
            self.browser.quit()
            raise NameError('FALHA')

    def __repr__(self):
        return f'{ "nome": "{self.url}", "usuario": "{self.usuario}" }'


class FirefoxColeta(ColetarRegistros):
    def __init__(self, url, usuario, senha):
        # Configurar o navegador
        profile = FirefoxProfile()
        profile.set_preference("browser.download.panel.shown", False)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference(
            'browser.download.manager.showWhenStarting', False)
        profile.set_preference("browser.download.dir",
                               "/home/info/Dev/converte_comunica_ponto")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "text/plain, application/octet-stream, application/binary,\
                               text/csv, application/csv, application/excel, text/comma-separated-values,\
                                   text/xml, application/xml")
        profile.accept_untrusted_certs = True
        
        # Instanciar o navegar firefox e inserir as configurações
        
        browser = Remote(
            # command_executor= 'http://127.0.0.1:4444/wd/hub',
            desired_capabilities= DesiredCapabilities.FIREFOX,
            browser_profile= profile
        )
        # browser = Firefox(profile)
        
        # Maximizar a tela do navegador
        browser.maximize_window()

        # Aumentar o tempo de timeout da resposta da pagina
        browser.implicitly_wait(30)        

        # Inserir os atributos para classe pai com uma instancia do navegador
        super().__init__(url, usuario, senha, browser)


class ChromeColeta(ColetarRegistros):
    def __init__(self, url, usuario, senha):
        options = ChromeOptions()
        preferecias = {'download.default_directory': '/home/info/Dev/converte_comunica_ponto',
                       'safebrowsing.enabled': 'false'}
        options.add_experimental_option('prefs', preferecias)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--start-maximized")
        browser = Chrome(options=options)
        browser.implicitly_wait(30)
        super().__init__(url, usuario, senha, browser)
