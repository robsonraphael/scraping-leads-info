# 📄 Raspagem de dados de vagas de emprego

Um projeto que automatiza a raspagem de dados de vagas de emprego no site [InfoJobs](https://www.infojobs.com.br/), coletando informações como título da vaga, empresa, local, salário, tipo de contratação e descrição, e salva os dados em um arquivo `.csv`.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* `selenium`: Automação de navegador
* `bs4 (BeautifulSoup)`: Extração de dados HTML
* `pandas`: Manipulação de dados
* `csv`: Escrita de arquivos CSV
* `logging`: Log de eventos

---

## 🗂️ Estrutura Geral do Código

### 1. **Configuração do Navegador**

```python
chrome_services = Service()
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=...')
driver = webdriver.Chrome(service=chrome_services, options=chrome_options)
```

> ⚙️ O navegador é configurado para rodar em **modo headless** (sem interface) e minimizar detecção de automação.

---

### 2. **Parâmetros de Busca**

```python
_vaga = 'Promotor Vendas'
_cidade = 'Recife - PE'
url = "https://www.infojobs.com.br/empregos-em-sao-paulo.aspx"
```

> Estes são os filtros de busca para a raspagem. Você pode alterar para qualquer vaga e cidade do Brasil.

---

### 3. **Interações com a Página**

* **Preenchimento de campos de busca**
* **Busca e clique na cidade**
* **Clique no botão de buscar**

> Todos os elementos são localizados usando `XPATH` ou `CSS Selectors`, com `WebDriverWait` para sincronização dinâmica da página.

---

### 4. **Scroll da Página**

```python
def scroll(driver, pausa: float, max_scroll: int=10)
```

> Executa o scroll da página até o final para carregar todas as vagas disponíveis dinamicamente.

---

### 5. **Extração dos Dados das Vagas**

```python
def achar_vagas() -> list[dict]
```

Esta função percorre todos os cards de vaga e extrai os seguintes campos:

* **VAGA**: Nome da vaga
* **EMPRESA**: Nome da empresa
* **LOCAL**: Local de trabalho
* **SALARIO**: Faixa salarial (se disponível)
* **TIPO**: Tipo da vaga (Home office, presencial)
* **DESCRIÇÃO**: Descrição da vaga
* **LINK\_VAGA**: Link direto para a vaga
* **LINK\_EMPRESA**: Link para o perfil da empresa (se houver)

> Obs: A função também clica dinamicamente em cada card para abrir o painel lateral com detalhes da vaga.

---

### 6. **Salva em CSV**

```python
data.to_csv(
    f"vaga-{_vaga}-{_cidade}-{datetime.today().date()}.csv",
    index=False,
    encoding='utf-8-sig',
    sep=';',
)
```

> Os dados coletados são salvos em um arquivo `.csv` com nome baseado nos parâmetros da busca.

---

## ✅ Requisitos para Execução

* Python 3.8+
* Google Chrome instalado
* Driver compatível com sua versão do Chrome (e adicionado ao PATH)

### Instalação de dependências:

```bash
pip install selenium beautifulsoup4 pandas
```

---

## 📎 Exemplo de Saída CSV

```csv
ID;VAGA;EMPRESA;LOCAL;SALARIO;TIPO;DESCRICAO;LINK_VAGA;LINK_EMPRESA
1;Promotor de Vendas;Empresa ABC;Recife - PE;R$ 1.800,00;CLT;"Atividades de promoção...";https://infojobs...;https://infojobs...
```
