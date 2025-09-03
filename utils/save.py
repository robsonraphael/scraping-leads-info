import pandas as pd
import csv
from datetime import datetime
from logs import log
import os

def to_csv(data_base: list, vaga: str, cidade: str):
    # Salvando em CSV
    if not data_base:
        log.logger.info("Lista de vagas está vazia ❌")
    else:
        # Criando DataFrame
        data = pd.DataFrame(data_base)

        # Salvando CSV
        name_csv = f"vaga-{(f"{vaga.split()[0]}-{vaga.split()[1]}") if len(vaga.split()) > 1 else vaga}-{cidade}-{datetime.today().date()}.csv"
        dir_path = os.path.join('csv')
        file_path = os.path.join(dir_path, name_csv)

        data.to_csv(
            file_path,
            index=False,
            encoding='utf-8-sig',
            sep=';',
            lineterminator='\n',
            quoting=csv.QUOTE_MINIMAL
        )