#Módulo para ler o site e obter os status das solicitações / Module to scrap the site and get the solicitations status

#Importações / Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

#Definir função / Define function
def scraper(navegador, fluigs):

  #Acessar a página da solciitação / Acess the solicition page
  navegador.get("http://fluig.raizeducacao.com.br/portal/p/01/pageworkflowview?app_ecm_workflowview_detailsProcessInstanceID=" + str(fluigs))
  #Garantir que a seção da página está totalmente carregada / Make sure that the page section is completely loaded
  WebDriverWait(navegador,20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="workflowView-cardViewer"]')))
  #Selecionar elemento com as informações das solicitações / Get the element with the solicitations information
  site_lancamento = navegador.find_element(By.XPATH, '//*[@id="workflowView-cardViewer"]')
  navegador.switch_to.frame(site_lancamento)

  #Definir listas auxiliares / Define auxiliary lists
  cancelado_str = []
  escondidos_str = []

  #Cada página possui elementos para cada um dos status. O status real é definido pelo elemento que não é da class 'hide'/
  #On every page, a element for each solicitation status can be found. The real solicitation status is defined by the element that does not have the 'hide' class

  #Obter o elemento que representa o status 'Cancelado' / Get the element with the 'Cancelled' status
  cancelado = (navegador.find_elements(By.CLASS_NAME, 'ativ-cancelado'))
  #Obter os elementos com class 'hide' / Get the elements with 'hide' class 
  escondidos = (navegador.find_elements(By.CLASS_NAME, 'hide'))

  #Converter variáveis selenium.webdriver.remote.webelement.WebElement para string / Convert 'selenium.webdriver.remote.webelement.WebElement' variables to string
  for i in range(len(cancelado)):
    cancelado_str.append(str(cancelado[i]))

  for i in range(len(escondidos)):
    escondidos_str.append(str(escondidos[i]))

  contagem = (escondidos_str.count(cancelado_str[0]))

  #Se o elemento 'cancelado' não está escondido na página, o chamada está, de fato, cancelado / If the 'cancelled' element is not hidden on the page, the solicitation is, in fact, cancelled
  if (contagem == 0):
    return 'CANCELADO'

  else:
    return 'ATIVO'