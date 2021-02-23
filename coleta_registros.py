#! python3
# -*- coding: utf-8 -*-
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located
)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
from time import sleep
from abc import ABC
import os

DIRETORIO = "/home/info/Dev/coleta_online/downloads"

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
        self.__wdw = WebDriverWait(self.browser, 120)
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
    
    @property
    def wdw(self):
        return self.__wdw
    
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
        arq = os.listdir(DIRETORIO)
        return "*.part" in arq or "*.crdownload" in arq
    
    def __terminou_download(self):
        terminou = self.__verifica_termino_download()
        tentativas = 0
            
        while terminou:
            tentativas += 1
            terminou = self.__verifica_termino_download()
            if tentativas >= 120:
                break

    def coleta_registros_registrador_henry(self):
        try:
            # Abre a pagina do registrador de ponto
            self.browser.get(self.url)

            # Locators para selectionar os itens
            locator_login = (By.ID, 'lblLogin')
            locator_senha = (By.ID, 'lblPass')
            locator_btn_entrar = (By.TAG_NAME, 'a')
            
            # Aguarda o carregamento dos itens
            self.wdw.until(
                presence_of_element_located(locator_login)
            )
            
            self.wdw.until(
                presence_of_element_located(locator_senha)
            )
            
            self.wdw.until(
                presence_of_element_located(locator_btn_entrar)
            )
            
            # Seleciona os campos e preenche para realizar login        
            self.browser.find_element(*locator_login).send_keys(self.usuario)
            self.browser.find_element(*locator_senha).send_keys(self.senha)
            self.browser.find_element(*locator_btn_entrar).click()

            # Clica no menu eventos
            locator_menu_events = (By.ID, 'divMenuEvents')
            
            self.wdw.until(
                presence_of_element_located(locator_menu_events)
            )
            
            self.browser.find_element(*locator_menu_events).click()

            # Clica no menu filtro
            locator_opc_filtro_por_data = (By.ID, 'menuItem2')
            
            self.wdw.until(
                presence_of_element_located(locator_opc_filtro_por_data)
            )
            
            self.browser.find_element(*locator_opc_filtro_por_data).click()
            
            periodos = self.__get_periodos_coleta()
                        
            # Preenche os campos de data
            self.browser.execute_script(
                f"document.querySelector('#lblDataI').value = '{periodos['inicio']}'")
            self.browser.execute_script(
                f"document.querySelector('#lblDataF').value = '{periodos['fim']}'")
            sleep(3)
            
            # Baixar o arquivo
            locator_btn_baixar = (By.CSS_SELECTOR, '#communication table a')
            
            self.wdw.until(
                presence_of_element_located(locator_btn_baixar)
            )
            
            botao_baixar = self.browser.find_elements(*locator_btn_baixar)
            botao_baixar[0].click()

            # Aguarda o termino do download
            self.__terminou_download()

            # Clica em sair
            botao_sair = self.browser.find_element_by_id('exitBtn')
            botao_sair.click()
            
            # Feche o browser                                    
            self.browser.quit()

        except Exception as erros:
            # print(f'Erros: {erros}')
            self.browser.quit()
            raise NameError('FALHA')

    def coleta_registros_registrador_controlId(self):
        try:
            self.browser.get(self.url)
            
            locator_usuario_input = (By.ID, 'input_user')
            locator_senha_input = (By.ID, 'input_password')
            locator_btn_logar = (By.ID, 'logar')
            
            self.wdw.until(presence_of_element_located(locator_usuario_input))
            self.wdw.until(presence_of_element_located(locator_senha_input))
            self.wdw.until(presence_of_element_located(locator_btn_logar))
            
            self.browser.find_element(*locator_usuario_input).send_keys(self.usuario)
            self.browser.find_element(*locator_senha_input).send_keys(self.senha)
            self.browser.find_element(*locator_btn_logar).click()
            
            sleep(5)
            locator_menu_afd = (By.CSS_SELECTOR, '#MasterPage_menu ul li:nth-child(4) a')            
            self.wdw.until(presence_of_element_located(locator_menu_afd))
            self.browser.find_element(*locator_menu_afd).click()
            
            sleep(5)         
            locator_por_data = (By.CSS_SELECTOR, 'a[modal="afd_data"]')
            self.wdw.until(presence_of_element_located(locator_por_data))
            self.browser.find_element(*locator_por_data).click()
            
            periodos = self.__get_periodos_coleta(False)
            
            sleep(5)
            locator_download = (By.CSS_SELECTOR, '.modal-footer button[class="btn green"]')
            self.wdw.until(presence_of_element_located(locator_download))
                        
            self.browser.execute_script(f"document.querySelector('#initial_date').value = '{periodos['inicio']}'")
            self.browser.find_element(*locator_download).click()
                    
            sleep(5)   
            self.__terminou_download()
            
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
        profile.set_preference("browser.download.dir", DIRETORIO)
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

        # Inserir os atributos para classe pai com uma instancia do navegador
        super().__init__(url, usuario, senha, browser)

class ChromeColeta(ColetarRegistros):
    def __init__(self, url, usuario, senha):
        options = ChromeOptions()
        preferecias = {'download.default_directory': DIRETORIO,
                       'safebrowsing.enabled': 'false'}
        options.add_experimental_option('prefs', preferecias)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--start-maximized")
        browser = Chrome(options=options)
        super().__init__(url, usuario, senha, browser)
