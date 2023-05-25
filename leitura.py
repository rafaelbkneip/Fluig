#Importações / Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

#Importar módulo / Import module
import cancelados_fluig

def pegar_dados(codigo, navegador):

  navegador.get("http://fluig.raizeducacao.com.br/portal/p/01/pageworkflowview?app_ecm_workflowview_detailsProcessInstanceID=" + str(codigo))
  aux = 0
  
  try:
    WebDriverWait(navegador,20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="workflowView-cardViewer"]')))
    informacoes = navegador.find_element(By.XPATH, '//*[@id="workflowView-cardViewer"]').get_attribute('src')
    
  #Determinar se a solicitação acessada é a última solicitação aberta ou apenas uma solcitação corrompida / Determine if the accessed solicitation is the last created solicitation or a corrupt one
  except:

    #Acessar a página das próximas seis solicitações / Access the page of the next six solicitations
    for i in range(1,7):

      #Página da solicitações / Solcitations page
      navegador.get("http://fluig.raizeducacao.com.br/portal/p/01/pageworkflowview?app_ecm_workflowview_detailsProcessInstanceID=" + str(codigo + i))

      try:
        WebDriverWait(navegador,25).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="workflowView-cardViewer"]')))
        informacoes = navegador.find_element(By.XPATH, '//*[@id="workflowView-cardViewer"]').get_attribute('src')

      #A cada erro na página, somar 1 ao contador / For each expection, add 1 to the counter 
      except:
        aux = aux + 1

    #Se é impossível ler todas as próximas seis páginas, essa é a última solicitação / If it is impossible to scrap all of the next six pages, this is last opened solicitation
    if(aux == 6):
      return "", "", "",  "", "", "", "", "", "", "", "", "", False,  ""
    
    #Se é possível ler algumas das páginas, a solicitação apenas está corrompida / If it is possible scrap any of the next six pages, the solicitation is just corrupt
    else:
      return "", "", "",  "", "", "", "", "", "", "", "", "", True, ""

  #Acessar informações da solicitação / Access the solicitation informations
  navegador.get(informacoes)

  protocolo = navegador.find_elements(By.XPATH, '//*[@id="secCabecalho"]/div/div[1]/div/label')

  #Solicitações do tipo 'Nº PROTOCOLO' e 'Reposição de Fundo Fixo' não são consideradas / 'Nº PROTOCOLO' and 'Reposição de Fundo Fixo' solicitiations are not considered
  if(protocolo[0].text =='Nº PROTOCOLO' or tipo_de_solicitacao[0].text == "Reposição de Fundo Fixo"):
    #Não retornar nenhuma informação dessa solicitação / Do not return any information of this solicitation
    return "", "", "", "", "", "", "", "", "", "", "", "", True, ""

  #Verificar se a solicitação está cancelada
  resultado = cancelados_fluig.scraper(navegador, codigo)
  if (resultado == "CANCELADO"):
    #Não retornar nenhuma informação dessa solicitação / Do not return any information of this solicitation
    return "", "", "", "", "", "", "", "", "", "", "", "", True, ""
    
  #Avaliar o tipo de solicitação
  #Caso na página da solicitação não seja possível localizar o elemento que contém essa informação, a solicitação não interessa / If it is not possible to find on the page that element that contais this information, the solicitation is not considered
  try:
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmFluig"]/div/div/div/h1')))
    tipo_de_solicitacao = navegador.find_elements(By.XPATH, '//*[@id="frmFluig"]/div/div/div/h1')

  except:
    #Não retornar nenhuma informação dessa solicitação / Do not return any information of this solicitation
    return "", "", "", "", "", "", "", "", "", "", "", "", True, ""

  #Depois das conferências cima, a solicitação está validada / After the above conferences, the solicitation is validated
  #Obter informações / Get informartions
  #Número da solicitação / Solicitation number
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secCabecalho"]/div/div[1]/div/span')))
  n_pedido = navegador.find_element(By.XPATH, '//*[@id="secCabecalho"]/div/div[1]/div/span').text

  print("Lendo o chamado: ", n_pedido)

  #Data / Date
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secCabecalho"]/div/div[2]/div/span')))
  data = navegador.find_element(By.XPATH, '//*[@id="secCabecalho"]/div/div[2]/div/span').text

  #Solicitante / Requester
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secSolicitante"]/div/div[1]/div/span[1]')))
  solicitante = navegador.find_element(By.XPATH, '//*[@id="secSolicitante"]/div/div[1]/div/span[1]').text 
    
  #Coligada / Related Company
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secUnidade"]/div[1]/div[1]/div/div/span[1]'))) 
  coligada = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div[1]/div[1]/div/div/span[1]').text   

  #Unidade/Filial - Branch
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secUnidade"]/div[1]/div[2]/div/div/span[1]'))) 
  unidade_filial = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div[1]/div[2]/div/div/span[1]').text

  #CAPEX
  WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secCabecalho"]/div/div[3]/div/span'))) 
  capex = navegador.find_element(By.XPATH, '//*[@id="secCabecalho"]/div/div[3]/div/span').text

  #A localização das informações abaixo varia de acordo com o tipo de solicitação / The location of the informations below varies depending on solicitation type
  if (tipo_de_solicitacao[0].text == "Solicitação de Reembolso"):

    #Centro de Custo
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secUnidade"]/div/div[3]/div/div/span[1]')))
    centro_de_custo = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div/div[3]/div/div/span[1]').text  

    #Natureza Orçamentária
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secInfoGeral"]/div[4]/div/table/tbody/tr[2]/td[4]/div/div/span[1]')))
    natureza_orcamentaria = navegador.find_element(By.XPATH,  '//*[@id="secInfoGeral"]/div[4]/div/table/tbody/tr[2]/td[4]/div/div/span[1]').text  

    #Fornecedor / Supplier
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secDeposito"]/div/div[3]/div[2]/div/span')))
    fornecedor = navegador.find_element(By.XPATH, '//*[@id="secDeposito"]/div/div[3]/div[2]/div/span').text 

    #Informações adicionais / Additional info
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secInfoGeral"]/div[4]/div/table/tbody/tr[2]/td[3]/div/span')))
    descricao =  navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[4]/div/table/tbody/tr[2]/td[3]/div/span').text 

    #Valor / Charged amount
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secInfoGeral"]/div[5]/div/table/tbody/tr[1]/td[2]/div/span')))
    valor = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[5]/div/table/tbody/tr[1]/td[2]/div/span').text

    #Vencimento / Due date
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[2]/div/span')))
    vencimento = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[2]/div/span').text

  if (tipo_de_solicitacao[0].text == "Solicitação de Adiantamento"):
    print(tipo_de_solicitacao[0].text)
    #Centro de custo / Cost center
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secUnidade"]/div[2]/div[1]/div/div/span[1]')))
    centro_de_custo = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div[2]/div[1]/div/div/span[1]').text  

    #Natrureza orçamentária / Budgetary nature
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="secUnidade"]/div[2]/div[2]/div/div/span[1]')))
    natureza_orcamentaria = navegador.find_element(By.XPATH,  '//*[@id="secUnidade"]/div[2]/div[2]/div/div/span[1]').text  

    #Fornecedor / Supplier
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[2]/div[1]/div[1]/div/span[1]')))

    try:
      fornecedor = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[1]/div[1]/div/span[1]').text
    except:
      fornecedor = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[1]/div[2]/div/span[1]').text 

    #Vencimento / Due date
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[3]/div[3]/div/span')))
    vencimento = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[3]/div[3]/div/span').text

    #Valor / Value amount
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[3]/div[1]/div/span'))) #//*[@id="secInfoGeral"]/div[3]/div[1]/div/span
    valor = navegador.find_element(By.XPATH,  '//*[@id="secInfoGeral"]/div[3]/div[1]/div/span').text 
      
    #Informações adicionais / Additional info
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secRodape"]/div/div/div/span')))
    descricao = navegador.find_element(By.XPATH, '//*[@id="secRodape"]/div/div/div/span').text

  if (tipo_de_solicitacao[0].text == "Solicitação de Pagamento"):
    #Centro de custo / Cost center
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secUnidade"]/div[2]/div[1]/div/div/span[1]')))
    centro_de_custo = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div[2]/div[1]/div/div/span[1]').text 

    #Natrureza orçamentária / Budgetary nature
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secUnidade"]/div[2]/div[2]/div/div/span[1]')))
    natureza_orcamentaria = navegador.find_element(By.XPATH, '//*[@id="secUnidade"]/div[2]/div[2]/div/div/span[1]').text
      
    #Fornecedor / Supplier
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[2]/div[1]/div[1]/div/span[1]')))

    try:
      fornecedor = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[1]/div[1]/div/span[1]').text
    except:
      fornecedor = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[2]/div[1]/div[2]/div/span[1]').text 

    #Valor / Charged amount
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[3]/div[1]/div/span')))
    valor =  navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[3]/div[1]/div/span').text

    #Informações adicionais / Additional info
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secRodape"]/div/div/div/span')))
    descricao = navegador.find_element(By.XPATH, '//*[@id="secRodape"]/div/div/div/span').text     

    #Vencimento / Due date
    WebDriverWait(navegador,20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="secInfoGeral"]/div[3]/div[4]/div/span')))                       
    vencimento = navegador.find_element(By.XPATH, '//*[@id="secInfoGeral"]/div[3]/div[4]/div/span').text

  #Retornar informações sobre a solicitação / Return the solicitation informations
  return  coligada, n_pedido, tipo_de_solicitacao[0].text, solicitante,  descricao, vencimento, valor, unidade_filial, centro_de_custo, natureza_orcamentaria, fornecedor, data, True, capex,