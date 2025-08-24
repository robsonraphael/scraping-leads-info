import scraper
from utils import output

# URL da raspagem
URL: str = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"

# Variaveis de busca
_vaga = 'Promotor Vendas'
_cidade = 'Recife - PE'

try:
    # Pesquis a pagina
    scraper.load_page(URL)

    # Espera toda a página carregar
    scraper.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Fecha a permissão de cookie
    scraper.close_cookie()

    # Pesquisa a vaga
    scraper.search_vaga(_vaga)

    # Busca e seleciona a cidade
    scraper.search_city(_cidade)

    # Esperar carregar
    scraper.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Scrolla a pagina ate o final
    scraper.scroll_page()
    
    # Percorre as vagas do site e adiciona na lista
    lista_de_vagas = scraper.get_vagas()

    # salva o arquivo csv
    output.save_to_csv(lista_de_vagas, _vaga, _cidade)
        
finally:
    scraper.quit()
