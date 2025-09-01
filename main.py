import core
import click
from rich.console import Console
from utils import save

# URL da raspagem
URL: str = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"

# Console
console = Console()

# Variaveis de busca
@click.command()
@click.option('--vaga', required=True, help="Vaga para buscar.")
@click.option('--cidade', default="São Paulo - SP", help="Cidade para filtrar.")

def main(vaga, cidade):
    "Scraping de leads INFO-JOBS"
    console.print("[bold blue]Iniciando scraping...[bold blue]")
    try:
        # Pesquisa a pagina
        core.load_page(URL)

        # Espera toda a página carregar
        core.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Fecha a permissão de cookie
        core.close_cookie()

        # Pesquisa a vaga
        core.search_vaga(vaga)
        # Busca e seleciona a cidade
        core.search_city(cidade)

        # Esperar carregar
        core.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
        # Scrolla a pagina ate o final
        core.scroll_page()
        
        # Percorre as vagas do site e adiciona na lista
        lista_de_vagas = core.get_vagas()

        # salva o arquivo csv
        save.to_csv(data_base=lista_de_vagas, vaga=vaga, cidade=cidade)
        console.print("[bold green]Scraping salvo [bold green]")
    finally:
        core.quit()
main()