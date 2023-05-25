#Importações / Imports
from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

#Importar módulos / Import modules
import login
import leitura

#Definir escopo da autorização / Define authorization scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#Definir planilha pelo seu ID e intervalo de células / Define spreadsheet by its ID and cell intervall
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = ''

#Acessar token de autorização / Access authorization token
creds = None
if os.path.exists('token.json'):
  creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('sheets', 'v4', credentials = creds)

#Acessar planilha e extrair valores / Access spreasheet and get values
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = SAMPLE_RANGE_NAME).execute()    

#Definir o número de solicitações na planilha / Define the number of solicitations on the sheet
fluigs = result['values']
valores = len(fluigs)
#Definir a última solicitação na planilha / Define the last solicitation of the sheet
codigo = int(fluigs[-1][0])

#Logar / Log in
navegador = login.login()

#Listas auxiliares / Auxiliart lists
lista_aux = []
lista = []

#Perimitir a leitura / Enable scraping
controle = True

while(controle):
    
    #Definir solicitações a serem lidas / Define solicitations to be scraped
    codigo = codigo + 1
    
    #Obter os dados da solicitação / Get solicitation information
    coligada, n_pedido, tipo_de_solicitacao, solicitante,  descricao, vencimento, valor, unidade_filial, centro_de_custo, natureza_orcamentaria, fornecedor, data, controle, capex = leitura.pegar_dados(codigo, navegador)
    
    #Caso a solicitação não exista e a anterior seja a última criada, definir um loop infinito para ler essa página repetidamente, até que essa solicitação seja criada
    #In case the solicitation does not exist and the previous one is the last one created, define an infinite loop to scrape this page constantly until the solicitation is created
    if(controle == False):
      codigo = codigo - 1
      controle = True

    #Validar as solicitações a serem consideradas / Solicitation validation
    if ():
      #Caso a solicitação seja de interesse, adicionar informações em uma lista / If the solicitation should be considered, information must be added to a list
      lista_aux.append(n_pedido)
      lista_aux.append(tipo_de_solicitacao)
      lista_aux.append(solicitante)
      lista_aux.append(descricao)
      lista_aux.append(vencimento)
      lista_aux.append(valor.split(" ")[1])
      lista_aux.append(unidade_filial)
      lista_aux.append(centro_de_custo)
      lista_aux.append(natureza_orcamentaria)
      lista_aux.append(fornecedor)
      lista_aux.append(data)
      lista_aux.append(data.split('/')[1])
      lista_aux.append(capex)

      #As informações devem ser inclúidas em uma lista bidimensional / Informations must be added to a two-dimensional list
      lista.append(lista_aux)

      #Definir a linha posterior a última linha da planilha / Define the row after the sheet's last row
      valores = valores + 1

      try: 
      #Escrever os resultados na planilha / Write the results on the sheet
        result = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, range ='Name!A' + str(valores) + ':N' + str((valores)), valueInputOption = 'USER_ENTERED', body = {'values': lista}).execute()

      except Exception as e:
        print(e)

      lista_aux = []
      lista = []