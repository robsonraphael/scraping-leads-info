import core
import click
import time
from rich.console import Console
from utils import save

# URL da raspagem
URL: str = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"

# Console
console = Console()

def search(vaga, cidade):
    "Executa uma Busca e extrai os dados."
    console.print(f"\n[bold blue]Iniciando scraping...[bold blue]")
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
        # reinicia o driver
        core.driver = core.webdriver.Chrome(service=core.chrome_services, options=core.chrome_options)

# Variaveis de busca
@click.command()
@click.option('--vaga', multiple=True, required=True, help="Vaga para buscar.")
@click.option('--cidade', default="São Paulo - SP", help="Cidade para filtrar.")

def main(vaga, cidade):
    "Scraping Info Jobs"
    try:
        # Se vaga e cidade forem fornecidas, executa uma única busca
        if len(vaga) == 1:
            search(vaga, cidade)
        else:
            with click.progressbar(vaga, label='Concluido') as bar:
                for vaga in bar:
                    core.driver.execute_script(f"window.open('{URL}','_blank');")
                    core.driver.switch_to.window(core.driver.window_handles[1])
                    search(vaga, cidade)
                    time.sleep(2)
    except Exception as e:
        console.print(f"[red]Erro geral: {e}[/red]")
    finally:
        core.quit()

if __name__ == "__main__":
    main()