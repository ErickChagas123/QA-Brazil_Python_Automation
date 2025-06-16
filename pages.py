#import
from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code
import time

# Definição da classe da página, dos localizadores e do método na classe
class UrbanRoutesPage:
    # Localizadores como atributos de classe

    #Endereço De e Para
    FROM_FIELD = (By.ID, 'from') #Endereço DE
    TO_FIELD = (By.ID, 'to') #Endereço PARA

    #Selecionar tarifa e chamar taxi
    TAXI_OPTION_LOCATOR = (By.XPATH, '//button[contains(text(),"Chamar")]')#Chamar taxi depois da localização
    COMFORT_ICON_LOCATOR = (By.XPATH, '//img[@src="/static/media/kids.075fd8d4.svg"]')#Icone do Comfort
    COMFORT_ACTIVE = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')#Clicar em Comfort

    #Numero de Telefone
    NUMBER_TEXT_LOCATOR = (By.CSS_SELECTOR, '.np-button')#Telefone
    NUMBER_DIGITAR = (By.ID, 'phone')
    NUMBER_CONFIRM = (By.CSS_SELECTOR, '.button.full')
    NUMBER_CODE = (By.ID, 'code')
    CODE_CONFIRM = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    NUMBER_FINISH = (By.CSS_SELECTOR, '.np-text')

    #METODO DE PAGAMENTO
    ADD_METODO_PAGAMENTO = (By.CSS_SELECTOR, '.pp-button.filled')#Botão de adicionar metodo de pagamento
    ADD_CARTAO = (By.CSS_SELECTOR, '.pp-plus')#Adicionar cartão no metodo de pagamento
    NUMERO_DO_CARTAO = (By.ID, 'number')#Numero do cartão
    CODIGO_DO_CARTAO = (By.CSS_SELECTOR, 'input.card-input#code')#Codigo de 2 digitos
    ADD_FINISH_CARTAO = (By.XPATH, '//button[contains(text(),"Adicionar")]')#Adicionar o cartão
    CLOSE_BUTTON_CARTAO = (By.CSS_SELECTOR,'.payment-picker.open .close-button')#Fechar o metodo de pagamento
    CONFIRM_CARTAO = (By.CSS_SELECTOR,'.pp-value-text')#Conferir se o valor mudou de Dinheiro para Cartão

    #ADICIONAR COMENTARIO
    ADD_COMENTARIO = (By.ID, 'comment')#Adicionar comentário
    SWITCH_COBERTOR = (By.CSS_SELECTOR,'.switch')#Botão do Switch
    SWITCH_COBERTOR_ACTIVE = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > input')
    ADD_SORVETE = (By.CSS_SELECTOR, '.counter-plus')#Adiciona Sorvete
    QNT_SORVETE = (By.CSS_SELECTOR, '.counter-value')#Quantidade de Sorvete
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR,'.smart-button')#Botão de chamar o taxi
    POP_UP = (By.CSS_SELECTOR, '.order-header-title')#Pop up do taxi

    def __init__(self, driver):
        self.driver = driver

#Locais "De" e "Para"
    def enter_from_location(self, from_text):
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.FROM_FIELD))
        self.driver.find_element(*self.FROM_FIELD).send_keys(from_text)

    def enter_to_location(self, to_text):
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.TO_FIELD))
        self.driver.find_element(*self.TO_FIELD).send_keys(to_text)

    def enter_locations(self, from_text, to_text):
        self.enter_from_location(from_text)
        self.enter_to_location(to_text)

    def get_from_location_value(self):
            return WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.FROM_FIELD)
            ).get_attribute('value')

    def get_to_location_value(self):
            return WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.TO_FIELD)
            ).get_attribute('value')

#Clicar em Chamar Táxi
    def click_taxi_option(self):
        self.driver.find_element(*self.TAXI_OPTION_LOCATOR).click()

#Clicar em Comfort
    def click_comfort_icon(self):
        self.driver.find_element(*self.COMFORT_ICON_LOCATOR).click()

    def click_comfort_active(self):
        try:
            active_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.COMFORT_ACTIVE))
            return "active" in active_button.get_attribute("class")
        except:
            return False

#Digitar o número
    def click_number_text(self, telefone):
        self.driver.find_element(*self.NUMBER_TEXT_LOCATOR).click() #Clica no número

        self.driver.find_element(*self.NUMBER_DIGITAR).send_keys(telefone)  #Digita o número

        self.driver.find_element(*self.NUMBER_CONFIRM).click() #Confirma o número

        code = retrieve_phone_code(self.driver) #Digita o código
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.NUMBER_CODE)
        )
        code_input.clear()
        code_input.send_keys(code)

        self.driver.find_element(*self.CODE_CONFIRM).click()#Confirma

    def numero_confirmado(self):
        numero = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.NUMBER_FINISH))
        return numero.text

#Botão metodo de pagamento
    #Botão metodo de pagamento
    def click_add_cartao(self,cartao,code):
        self.driver.find_element(*self.ADD_METODO_PAGAMENTO).click()
        self.driver.find_element(*self.ADD_CARTAO).click()
        WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(self.NUMERO_DO_CARTAO))
        self.driver.find_element(*self.NUMERO_DO_CARTAO).send_keys(cartao)
        WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(self.CODIGO_DO_CARTAO))
        self.driver.find_element(*self.CODIGO_DO_CARTAO).send_keys(code)
        WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(self.ADD_FINISH_CARTAO))
        self.driver.find_element(*self.ADD_FINISH_CARTAO).click()
        self.driver.find_element(*self.CLOSE_BUTTON_CARTAO).click()

    def confirm_cartao(self):
        return self.driver.find_element(*self.CONFIRM_CARTAO).text

#Adicionar comentario
    def add_comentario(self, comentario):
        self.driver.find_element(*self.ADD_COMENTARIO).send_keys(comentario)

    def coment_confirm(self):
        return self.driver.find_element(*self.ADD_COMENTARIO).get_attribute('value')

#Switch do cobertor
    def switch_cobertor(self):
        switch_ativo = self.driver.find_element(*self.SWITCH_COBERTOR)
        switch_ativo.click()

    def switch_cobertor_active(self):
        switch = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SWITCH_COBERTOR_ACTIVE))
        return switch.is_selected()

#Adicionar sorvete
    def add_ice(self):
        self.driver.find_element(*self.ADD_SORVETE).click()

#Quantidade de sorvete
    def qnt_sorvete(self):
        return self.driver.find_element(*self.QNT_SORVETE).text

#Finalizar e chamar o taxi
    def call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def pop_up_show(self):
        pop_up = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.POP_UP))
        return pop_up.text
