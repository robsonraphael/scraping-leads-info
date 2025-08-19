from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

# ==========================
# CONFIGURAÇÃO DO SELENIUM
# ==========================
chrome_services = Service()
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes')
#chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--disable-gpu")  # Desativa aceleração por GPU
chrome_options.add_argument("--headless=new")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
#chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument("--disable-popup-blocking")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-infobars")
#chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Evita detecção

# Carrega o navegador
driver = webdriver.Chrome(service=chrome_services, options=chrome_options)
# URL da raspagem
url: str = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"

# Função para aguardar
wait = WebDriverWait(driver, 10)

try:
    driver.get(url)

    # Espera toda a página carregar
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Fecha a permissão de cookie
    driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()

    # Pesquisa a vaga
    def buscar_vaga(search: str) -> None:
        input_field = driver.find_element(By.CSS_SELECTOR, 'input[id="keywordsCombo"]')
        input_field.send_keys(search)
    buscar_vaga('python')

    # Busca e seleciona a cidade
    def buscar_cidade(search: str) -> None:
        input_field = driver.find_element(By.CSS_SELECTOR, 'input[id="city"]')
        input_field.clear()        
        input_field.send_keys(search)

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[3]/div[2]/div/div[2]/div/div[2]')))
        
        city = driver.find_element(By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[3]/div[2]/div/div[2]/div/div[2]')
        city.click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[4]/a')))

        btn = driver.find_element(By.XPATH, '//*[@id="searchHeader"]/div[1]/div/div[1]/div[4]/a')
        btn.click()
    buscar_cidade('Recife - PE')

    # Esperar carregar
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Scrolla a pagina ate o final
    def scroll(driver, pausa: float, max_scroll: int=10) -> None:
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        scroll_count = 0

        while scroll_count < max_scroll:
            # scrolla até o final
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Espera carregar
            time.sleep(pausa)
            # retorna
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Saida
            last_height = new_height
            scroll_count += 1
    scroll(driver, 1.5)
    
    # Percorre as vagas do site e adiciona na lista
    def achar_vagas() -> list:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        list_cards = soup.find_all('div', class_='card')
        dados_vagas: list = []
        count = 1

        if not list_cards:        
            print("Nenhum Card encontrado")

        for card in list_cards:
            # Click nos cards da vaga e pega os dados
            if "js_rowCard" in card['class']:
                # Nome e link da vaga  
                name_vaga = card.find('h2')
                if not name_vaga:
                    name_vaga = "N/A"
                    link_vaga = "N/A"
                else:
                    link_vaga = name_vaga.parent
                    link_vaga = link_vaga.get('href')
                    name_vaga = name_vaga.get_text().strip()
            
                # Nome e link da empresa
                name_empresa = card.find('div', class_='d-flex align-items-baseline')
                if not name_empresa:
                    name_empresa = "N/A"
                    link_empresa = "N/A"
                else:
                    if name_empresa.find('a'):
                        link_empresa = name_empresa.find('a')['href']
                        name_empresa = name_empresa.find('a').get_text().strip()
                    else:
                        name_empresa = name_empresa.find('div', class_='text-body').get_text().strip() if name_empresa.find('div', class_='text-body') else "N/A"
                        link_empresa = "N/A"
                
                # vacancy
                if not 'active' in card['class'] and 'active' not in card['class']: 
                    element = card.find('div')
                    driver.find_element(By.ID, element['id']).click()
                    wait.until(EC.presence_of_element_located((By.ID, 'vacancylistDetail')))
                    try:
                        div_vacancy = driver.find_element(By.XPATH, '//*[@id="vacancylistDetail"]')   
                        
                        # Local
                        local_vaga = div_vacancy.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div[1]/div[2]/div[1]')
                        local_vaga = local_vaga.text.strip()
                        time.sleep(0.3)
                        
                        # Salario
                        salario_vaga = div_vacancy.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div[1]/div[2]/div[2]')
                        salario_vaga = salario_vaga.text.strip()
                        time.sleep(0.3)

                        # Tipo
                        tipo_vaga = div_vacancy.find_element(By.XPATH, '//*[@id="VacancyHeader"]/div[1]/div[1]/div[2]/div[3]')
                        tipo_vaga = tipo_vaga.text.strip()
                        time.sleep(0.3)

                        # descricao
                        descricao_vaga = div_vacancy.find_element(By.XPATH, '//*[@id="vacancylistDetail"]/div[2]')
                        descricao_vaga = descricao_vaga.text.strip()
                        time.sleep(0.3)

                        print(f"Dados da vaga {count} extraido ✅")

                    except Exception as e:
                        print(f"Erro ao extrair dados da vaga {count}")
                        #print(e)
                        salario_vaga, local_vaga, tipo_vaga, descricao_vaga = "N/A", "N/A", "N/A", "N/A"

                else:
                    continue
            
                # Cria o objeto 
                obj_vaga = {
                    'ID': count,
                    'VAGA': name_vaga,
                    'EMPRESA': name_empresa,
                    'LOCAL': local_vaga,
                    'SALARIO': salario_vaga,
                    'TIPO': tipo_vaga,
                    'DESCRICAO': descricao_vaga,
                    'LINK_VAGA': link_vaga,
                    'LINK_EMPRESA': link_empresa
                }
                    
                # Adiciona o obj_vaga a lista de vagas
                dados_vagas.append(obj_vaga)
                count += 1
    
        return dados_vagas
    #Execução
    lista_vagas = achar_vagas()

    # Salvando em CSV
    if not lista_vagas:
        print("Nenhuma Vaga na lista")
    else:
        # Criando DataFrame
        data = pd.DataFrame(lista_vagas)

        # Salvando CSV
        data.to_csv(
            "vagas_python.csv",
            index=False,
            encoding='utf-8-sig',
            sep=';',
            lineterminator='\n',
            quoting=csv.QUOTE_MINIMAL
        )
finally:
    driver.quit()
