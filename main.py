from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

# ==========================
# CONFIGURAÇÃO DO SELENIUM
# ==========================
chrome_options = Options()
chrome_services = Service()
# Ignorar erro SSL
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
#chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")  # Desativa aceleração por GPU
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")

# Carrega o navegador
driver = webdriver.Chrome(service=chrome_services, options=chrome_options)
# URL da raspagem
url = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"

# Função para aguardar
wait = WebDriverWait(driver, 10)

try:
    driver.get(url)

    # Espera toda a página carregar
    wait.until(lambda d: d.execute_script(
        'return document.readyState') == 'complete')

    # Fecha a permissão de cookie
    driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()

    # Pesquisa a vaga
    def search(search: str):
        input_search_tag = driver.find_element(
            By.XPATH, '//*[@id="keywordsCombo"]')
        for c in search:
            input_search_tag.send_keys("".join(c))
    search('python')

    time.sleep(0.3)

    # Filtra e seleciona a cidade
    def search_city(search: str):
        input_search_tag = driver.find_element(By.XPATH, '//*[@id="city"]')
        input_search_tag.clear()        
        for c in search:
            input_search_tag.send_keys("".join(c))
        time.sleep(0.3)

        city = driver.find_element(
            By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[3]/div[2]/div/div[2]/div/div[2]')
        city.click()
        time.sleep(0.4)

        btn = driver.find_element(
            By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[4]/a')
        btn.click()
    search_city('Recife - PE')

    # Esperar carregar
    wait.until(lambda d: d.execute_script(
        'return document.readyState') == 'complete')

    # Scrolla a pagina ate o final
    def scroll(driver, pausa, max_scroll=10):
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_count = 0

        while scroll_count < max_scroll:
            # Rolar até o final
            driver.execute_script(
                "window.scrollTo(1, document.body.scrollHeight);")
            # Espera carregar
            time.sleep(pausa)
            # retorna
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break  # Saida
            last_height = new_height
            scroll_count += 1
    scroll(driver, pausa=2, max_scroll=10)

    # Percorre as vagas do site e adiciona na lista
    def achar_vagas():
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        list_cards = soup.find_all('div', class_='card')
        dados_vagas = []
        count = 1
    
        for card in list_cards:
            # Nome e link da vaga  
            name_vaga = card.find('h2')
            if not name_vaga:
                name_vaga = ""
            else:
                link_vaga = name_vaga.parent
                link_vaga = link_vaga.get('href')
                name_vaga = name_vaga.get_text().strip()
                #print(name_vaga)
                #print(link_vaga, '\n')
            
            # Nome e link da empresa
            name_empresa = card.find('div', class_='d-flex align-items-baseline')
            if not name_empresa:
                name_empresa = ""
            else:
                if name_empresa.find('a'):
                    link_empresa = name_empresa.find('a')['href']
                    name_empresa = name_empresa.find('a').get_text().strip()
                    #print(name_empresa)
                    #print(link_vaga,'\n')

            # Clickar nos cards e pegar o local e salario da vaga
            if "js_rowCard" in card['class']:
                if not 'active' in card['class']: 
                    element = card.find('div')
                    driver.find_element(By.ID, element['id']).click()
                    time.sleep(0.2)
                    try:
                        salario_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[2]').text.strip()
                        local_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[1]').text.strip()
                        tipo_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[3]').text.strip()
                        descricao_vaga = driver.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]').text.strip()
                        
                        #print(tipo_vaga.text.strip())
                        #print(local_vaga.text.strip())
                        #print(salario_vaga.text.strip())
                        #print(descricao_vaga)
                    except:
                        ""

                if 'active' in card['class']:
                    salario_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[2]').text.strip()
                    local_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[1]').text.strip()
                    tipo_vaga = driver.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div/div[2]/div[3]').text.strip()
                    descricao_vaga = driver.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]').text.strip()

                    #print(tipo_vaga.text.strip())
                    #print(local_vaga.text.strip())
                    #print(salario_vaga.text.strip())
            
            obj_vaga = {
                'id': count,
                'title': name_vaga,
                'empesa': name_empresa,
                'local': local_vaga,
                'salario': salario_vaga,
                'tipo': tipo_vaga,
                'descricao': [descricao_vaga],
                'links': {
                    'vaga': link_vaga,
                    'empresa': link_empresa,
                }
            }
            
            dados_vagas.append(obj_vaga)
            count += 1

        return dados_vagas
    lista_vagas = achar_vagas()
    
    data = pd.DataFrame(lista_vagas)
    data.to_csv("vagas-python2.csv", index=False, encoding='utf-8')
finally:
    driver.quit()
