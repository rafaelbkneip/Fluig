#Módulo para logar no site / Module to log in to the website

#Importações / Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import selenium.webdriver.support.expected_conditions as EC

#Definir configurações da janela do Google Chrome / Define Google Chrome tab configurations
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

#Definir função / Define function
def login():
    #Acessar portal / Access website
    navegador = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    navegador.get("http://fluig.raizeducacao.com.br/portal/home")

    #Logar / Log in
    username = navegador.find_element(By.ID, "username")
    username.send_keys("")
    password = navegador.find_elements(By.ID, "password")[-1]
    password.send_keys("")
    botao=navegador.find_element(By.ID, "submitLogin")
    botao.click()

    return navegador